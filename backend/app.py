from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
SCANNERS = ("checkov", "trivy", "kubescape")
STAGES = ("raw", "normalised", "matched", "metrics")

app = FastAPI(title="Scanner Benchmark API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http://(127\.0\.0\.1|localhost):\d+$",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class RunRequest(BaseModel):
    case_id: str = Field(min_length=1)
    scanners: list[Literal["checkov", "trivy", "kubescape"]] = Field(min_length=1)
    matching_mode: Literal["review", "strict"] = "review"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict | list:
    if not path.exists():
        raise HTTPException(404, f"File not found: {path.relative_to(PROJECT_ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise HTTPException(500, f"Invalid JSON in {path.name}: {exc}") from exc


def case_dir(case_id: str) -> Path:
    for base in ("kubernetes", "helm", "dockerfiles"):
        candidate = PROJECT_ROOT / "corpus" / base / case_id
        if candidate.is_dir():
            return candidate
    raise HTTPException(404, f"Benchmark case not found: {case_id}")


def artifact_path(directory: Path) -> Path:
    for name in ("artifact.yaml", "artifact.yml", "Dockerfile"):
        candidate = directory / name
        if candidate.exists():
            return candidate
    raise HTTPException(404, f"No artifact found in {directory.name}")


def output_path(stage: str, scanner: str, case_id: str) -> Path:
    suffix = {
        "raw": ".json",
        "normalised": ".normalised.json",
        "matched": ".matched.json",
        "metrics": ".metrics.json",
    }[stage]
    return PROJECT_ROOT / "results" / stage / scanner / f"{case_id}{suffix}"


def safe_report(name: str) -> Path:
    base = (PROJECT_ROOT / "results" / "reports").resolve()
    path = (base / name).resolve()
    if base not in path.parents or path.suffix.lower() != ".md":
        raise HTTPException(400, "Invalid report name")
    return path


def standard_metrics(scanner: str, case_id: str, data: dict) -> dict:
    nested = data.get("data") if isinstance(data.get("data"), dict) else {}
    metrics = data.get("metrics")
    if not isinstance(metrics, dict):
        metrics = nested.get("metrics")
    if not isinstance(metrics, dict):
        metrics = data
    counts = data.get("counts")
    if not isinstance(counts, dict):
        counts = nested.get("counts")
    if not isinstance(counts, dict):
        counts = metrics.get("counts")
    if not isinstance(counts, dict):
        counts = {}
    return {
        "scanner": scanner,
        "case_id": data.get("case_id", nested.get("case_id", case_id)),
        "counts": {
            "true_positive_count": counts.get("true_positive_count", counts.get("tp", data.get("true_positive_count", 0))),
            "false_positive_count": counts.get("false_positive_count", counts.get("fp", data.get("false_positive_count", 0))),
            "false_negative_count": counts.get("false_negative_count", counts.get("fn", data.get("false_negative_count", 0))),
            "unlabelled_extra_findings_count": counts.get("unlabelled_extra_findings_count", counts.get("unlabelled_extra_count", data.get("unlabelled_extra_findings_count", 0))),
        },
        "metrics": {
            "precision": metrics.get("precision"),
            "recall": metrics.get("recall"),
            "f1_score": metrics.get("f1_score", metrics.get("f1")),
        },
    }


def command(args: list[str], acceptable=(0,), timeout=300) -> str:
    result = subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    if result.returncode not in acceptable:
        detail = (result.stderr or result.stdout or "No output").strip()
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(args)}\n{detail[-3500:]}")
    return "\n".join(x for x in (result.stdout.strip(), result.stderr.strip()) if x)


def python_script(name: str) -> str:
    path = PROJECT_ROOT / "scripts" / name
    if not path.exists():
        raise RuntimeError(f"Required script missing: scripts/{name}")
    return command([sys.executable, str(path)])


def scanner_command(scanner: str, case_id: str) -> str:
    directory = case_dir(case_id)
    artifact = artifact_path(directory)
    raw = output_path("raw", scanner, case_id)
    raw.parent.mkdir(parents=True, exist_ok=True)

    if scanner == "checkov":
        exe = shutil.which("checkov")
        if not exe:
            for candidate in (PROJECT_ROOT / ".venv" / "Scripts" / "checkov.CMD", PROJECT_ROOT / ".venv" / "Scripts" / "checkov.exe"):
                if candidate.exists():
                    exe = str(candidate)
                    break
        if not exe:
            raise RuntimeError("Checkov not found. Activate .venv and install Checkov.")
        result = subprocess.run([exe, "--file", str(artifact), "--framework", "kubernetes", "--output", "json"], cwd=PROJECT_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
        if result.returncode not in (0, 1) or not result.stdout.strip():
            raise RuntimeError(result.stderr.strip() or "Checkov returned no JSON")
        raw.write_text(result.stdout, encoding="utf-8")
        version = command([exe, "--version"])
        (raw.parent / "checkov-version.txt").write_text(version, encoding="utf-8")
        return "Checkov scan completed."

    if scanner == "trivy":
        exe = PROJECT_ROOT / "tools" / "trivy" / "trivy.exe"
        if not exe.exists():
            raise RuntimeError("Trivy not found at tools/trivy/trivy.exe")
        output = command([str(exe), "config", str(directory), "--format", "json", "--output", str(raw)])
        (raw.parent / "trivy-version.txt").write_text(command([str(exe), "--version"]), encoding="utf-8")
        return output or "Trivy scan completed."

    tools = PROJECT_ROOT / "tools" / "kubescape"
    candidates = [tools / "kubescape.exe", tools / "kubescape_4.0.10_windows_amd64.exe", *sorted(tools.glob("*windows_amd64*.exe"))]
    exe = next((x for x in candidates if x.exists()), None)
    if not exe:
        raise RuntimeError("Kubescape not found under tools/kubescape/")
    output = command([str(exe), "scan", str(directory), "--format", "json", "--output", str(raw)], acceptable=(0, 1))
    (raw.parent / "kubescape-version.txt").write_text(command([str(exe), "version"]), encoding="utf-8")
    return output or "Kubescape scan completed."


def run_pipeline(scanner: str, case_id: str) -> dict:
    try:
        runner = PROJECT_ROOT / "scripts" / f"run_case001_{scanner}_pipeline.py"
        if case_id == "case-001-privileged-container" and runner.exists():
            log = python_script(runner.name)
        else:
            if case_id != "case-001-privileged-container":
                raise RuntimeError("Current processing scripts are hard-coded for case-001. Parameterise them before running additional cases.")
            parts = []
            if (PROJECT_ROOT / "scripts" / "validate_case.py").exists():
                parts.append(python_script("validate_case.py"))
            parts.append(scanner_command(scanner, case_id))
            for name in (f"normalize_{scanner}.py", f"match_{scanner}_to_ground_truth.py", f"compute_metrics_{scanner}.py", f"generate_case001_{scanner}_report.py"):
                parts.append(python_script(name))
            log = "\n".join(x for x in parts if x)
        path = output_path("metrics", scanner, case_id)
        metrics = standard_metrics(scanner, case_id, read_json(path)) if path.exists() else None
        return {"scanner": scanner, "status": "completed", "console_output": log, "metrics": metrics}
    except (RuntimeError, subprocess.TimeoutExpired, HTTPException) as exc:
        return {"scanner": scanner, "status": "failed", "console_output": "", "error": str(exc), "metrics": None}


@app.get("/api/health")
def health() -> dict:
    return {"status": "online", "project": "Scanner Benchmark API", "time": now()}


@app.get("/api/cases")
def cases() -> dict:
    root = PROJECT_ROOT / "corpus"
    rows = []
    for kind, folder in (("kubernetes", root / "kubernetes"), ("helm", root / "helm"), ("dockerfile", root / "dockerfiles")):
        if not folder.exists():
            continue
        for directory in sorted(x for x in folder.iterdir() if x.is_dir()):
            artifact = next((directory / n for n in ("artifact.yaml", "artifact.yml", "Dockerfile") if (directory / n).exists()), None)
            truth = directory / "ground_truth.yaml"
            severity = None
            if truth.exists():
                try:
                    parsed = yaml.safe_load(truth.read_text(encoding="utf-8-sig")) or {}
                    items = parsed.get("misconfigurations", [])
                    severity = items[0].get("severity") if items else None
                except (yaml.YAMLError, OSError):
                    pass
            rows.append({"case_id": directory.name, "artifact_type": kind, "artifact_name": artifact.name if artifact else None, "ground_truth_name": truth.name if truth.exists() else None, "severity": severity, "validation_status": "valid" if artifact and truth.exists() else "incomplete"})
    return {"cases": rows}


@app.get("/api/metrics/{scanner}")
def metrics(scanner: str, case_id: str = Query("case-001-privileged-container")) -> dict:
    if scanner not in SCANNERS:
        raise HTTPException(400, f"Unsupported scanner: {scanner}")
    path = output_path("metrics", scanner, case_id)
    data = standard_metrics(scanner, case_id, read_json(path))
    data["updated_at"] = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
    return data


@app.get("/api/outputs/{stage}/{scanner}")
def outputs(stage: str, scanner: str, case_id: str = Query("case-001-privileged-container")) -> dict:
    if stage not in STAGES:
        raise HTTPException(400, f"Unsupported stage: {stage}")
    if scanner not in SCANNERS:
        raise HTTPException(400, f"Unsupported scanner: {scanner}")
    path = output_path(stage, scanner, case_id)
    return {"stage": stage, "scanner": scanner, "case_id": case_id, "data": read_json(path)}


@app.get("/api/reports")
def reports() -> dict:
    folder = PROJECT_ROOT / "results" / "reports"
    if not folder.exists():
        return {"reports": []}
    rows = [{"name": path.name, "modified_at": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(), "size_bytes": path.stat().st_size} for path in sorted(folder.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)]
    return {"reports": rows}


@app.get("/api/reports/{name}", response_class=PlainTextResponse)
def report(name: str) -> str:
    path = safe_report(name)
    if not path.exists():
        raise HTTPException(404, "Report not found")
    return path.read_text(encoding="utf-8-sig")


@app.post("/api/run")
def run(request: RunRequest) -> dict:
    case_dir(request.case_id)
    selected = list(dict.fromkeys(request.scanners))
    return {"case_id": request.case_id, "matching_mode": request.matching_mode, "started_at": now(), "results": [run_pipeline(scanner, request.case_id) for scanner in selected]}


if not FRONTEND_DIR.exists():
    raise RuntimeError(f"Frontend directory not found: {FRONTEND_DIR}")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
