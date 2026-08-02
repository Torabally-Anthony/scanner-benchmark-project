from __future__ import annotations

import base64
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Project paths and constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
CONFIG_PATH = PROJECT_ROOT / "config" / "benchmark_config.yaml"

SCANNERS = (
    "checkov",
    "trivy",
    "kubescape",
)

OUTPUT_STAGES = (
    "raw",
    "normalised",
    "matched",
    "metrics",
)

MATCHING_MODES = (
    "review",
    "strict",
)


ARTIFACT_SETTINGS: dict[str, dict[str, Any]] = {
    "kubernetes_yaml": {
        "label": "Kubernetes YAML",
        "corpus_folder": "kubernetes",
        "runner": "run_benchmark.py",
        "applicable_scanners": (
            "checkov",
            "trivy",
            "kubescape",
        ),
        "normalised_root": "results/normalised_generic",
        "matched_root": "results/matched_generic",
        "metrics_root": "results/metrics_generic",
        "reports_root": "results/reports_generic",
    },
    "dockerfile": {
        "label": "Dockerfile",
        "corpus_folder": "dockerfiles",
        "runner": "run_dockerfile_benchmark.py",
        "applicable_scanners": (
            "checkov",
            "trivy",
        ),
        "normalised_root": "results/normalised_dockerfile",
        "matched_root": "results/matched_dockerfile",
        "metrics_root": "results/metrics_dockerfile",
        "reports_root": "results/reports_dockerfile",
    },
    "helm_chart": {
        "label": "Helm chart",
        "corpus_folder": "helm",
        "runner": "run_helm_benchmark.py",
        "applicable_scanners": (
            "checkov",
            "trivy",
            "kubescape",
        ),
        "normalised_root": "results/normalised_helm",
        "matched_root": "results/matched_helm",
        "metrics_root": "results/metrics_helm",
        "reports_root": "results/reports_helm",
    },
}


REPORT_ROOTS: dict[str, Path] = {
    "kubernetes_yaml": (
        PROJECT_ROOT / "results" / "reports_generic"
    ),
    "dockerfile": (
        PROJECT_ROOT / "results" / "reports_dockerfile"
    ),
    "helm_chart": (
        PROJECT_ROOT / "results" / "reports_helm"
    ),
    "comparison": (
        PROJECT_ROOT / "results" / "comparison"
    ),
}


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Scanner Benchmark API",
    description=(
        "Backend API for processing and reviewing Kubernetes YAML, "
        "Dockerfile and Helm scanner benchmark results."
    ),
    version="2.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=(
        r"^https?://"
        r"(127\.0\.0\.1|localhost)"
        r"(:\d+)?$"
    ),
    allow_credentials=False,
    allow_methods=[
        "GET",
        "POST",
        "OPTIONS",
    ],
    allow_headers=[
        "Content-Type",
    ],
)


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

ScannerName = Literal[
    "checkov",
    "trivy",
    "kubescape",
]

MatchingMode = Literal[
    "review",
    "strict",
]


class ProcessRequest(BaseModel):
    """Request for processing saved scanner outputs."""

    case_id: str = Field(
        min_length=1,
        description="Configured benchmark case ID.",
    )

    scanners: list[ScannerName] | None = Field(
        default=None,
        description=(
            "Scanners to process. When omitted, all scanners "
            "applicable to the selected artifact type are processed."
        ),
    )

    matching_mode: MatchingMode = Field(
        default="review",
        description=(
            "Review mode keeps unmapped findings as unlabelled extras. "
            "Strict mode treats them as false positives."
        ),
    )


# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------

def utc_now() -> str:
    """Return the current UTC time."""

    return datetime.now(
        timezone.utc
    ).isoformat()


def modified_time(path: Path) -> str:
    """Return a file modification time in UTC."""

    return datetime.fromtimestamp(
        path.stat().st_mtime,
        timezone.utc,
    ).isoformat()


def relative_path(path: Path) -> str:
    """Return a path relative to the project root."""

    try:
        return str(
            path.relative_to(PROJECT_ROOT)
        )

    except ValueError:
        return str(path)


def resolve_project_path(
    path_value: Any,
    field_name: str,
) -> Path:
    """
    Resolve a project-relative path and ensure it does not
    escape the project directory.
    """

    if not isinstance(path_value, str):
        raise HTTPException(
            status_code=500,
            detail=(
                f"Configuration field '{field_name}' "
                "must be a string."
            ),
        )

    clean_value = path_value.strip()

    if not clean_value:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Configuration field '{field_name}' "
                "cannot be empty."
            ),
        )

    path = (
        PROJECT_ROOT / clean_value
    ).resolve()

    try:
        path.relative_to(
            PROJECT_ROOT.resolve()
        )

    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Configuration path '{field_name}' "
                "must remain inside the project."
            ),
        ) from error

    return path


def read_json(path: Path) -> dict[str, Any] | list[Any]:
    """Read a JSON file."""

    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail=(
                "File not found: "
                f"{relative_path(path)}"
            ),
        )

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Invalid JSON in "
                f"{relative_path(path)}: {error}"
            ),
        ) from error

    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not read "
                f"{relative_path(path)}: {error}"
            ),
        ) from error


def read_yaml(path: Path) -> dict[str, Any]:
    """Read a YAML mapping."""

    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail=(
                "File not found: "
                f"{relative_path(path)}"
            ),
        )

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            data = yaml.safe_load(file) or {}

    except yaml.YAMLError as error:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Invalid YAML in "
                f"{relative_path(path)}: {error}"
            ),
        ) from error

    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not read "
                f"{relative_path(path)}: {error}"
            ),
        ) from error

    if not isinstance(data, dict):
        raise HTTPException(
            status_code=500,
            detail=(
                f"Expected a YAML mapping in "
                f"{relative_path(path)}."
            ),
        )

    return data


# ---------------------------------------------------------------------------
# Configuration and case helpers
# ---------------------------------------------------------------------------

def load_benchmark_config() -> dict[str, Any]:
    """Load benchmark_config.yaml."""

    if not CONFIG_PATH.is_file():
        raise HTTPException(
            status_code=500,
            detail=(
                "Benchmark configuration not found: "
                f"{relative_path(CONFIG_PATH)}"
            ),
        )

    configuration = read_yaml(
        CONFIG_PATH
    )

    cases = configuration.get("cases")

    if not isinstance(cases, dict):
        raise HTTPException(
            status_code=500,
            detail=(
                "benchmark_config.yaml does not contain "
                "a valid 'cases' mapping."
            ),
        )

    return configuration


def normalise_artifact_type(
    value: Any,
) -> str:
    """Return one recognised artifact type."""

    artifact_type = str(
        value or ""
    ).strip().lower()

    aliases = {
        "kubernetes": "kubernetes_yaml",
        "k8s": "kubernetes_yaml",
        "kubernetes_yaml": "kubernetes_yaml",
        "docker": "dockerfile",
        "dockerfile": "dockerfile",
        "helm": "helm_chart",
        "helm_chart": "helm_chart",
    }

    normalised = aliases.get(
        artifact_type
    )

    if normalised is None:
        raise HTTPException(
            status_code=500,
            detail=(
                "Unsupported artifact type in configuration: "
                f"'{artifact_type}'."
            ),
        )

    return normalised


def get_case_configuration(
    case_id: str,
) -> tuple[dict[str, Any], str]:
    """Return one configured case and its artifact type."""

    configuration = load_benchmark_config()

    cases = configuration["cases"]

    case_configuration = cases.get(
        case_id
    )

    if not isinstance(
        case_configuration,
        dict,
    ):
        raise HTTPException(
            status_code=404,
            detail=(
                f"Benchmark case not found: {case_id}"
            ),
        )

    artifact_type = normalise_artifact_type(
        case_configuration.get(
            "artifact_type"
        )
    )

    return (
        case_configuration,
        artifact_type,
    )


def applicable_scanners(
    artifact_type: str,
) -> tuple[str, ...]:
    """Return scanners applicable to an artifact type."""

    settings = ARTIFACT_SETTINGS.get(
        artifact_type
    )

    if settings is None:
        raise HTTPException(
            status_code=500,
            detail=(
                f"No artifact settings exist for "
                f"'{artifact_type}'."
            ),
        )

    return tuple(
        settings["applicable_scanners"]
    )


def validate_scanner(
    scanner: str,
) -> str:
    """Validate a scanner name."""

    scanner = scanner.strip().lower()

    if scanner not in SCANNERS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported scanner: {scanner}"
            ),
        )

    return scanner


def ensure_scanner_applicable(
    scanner: str,
    artifact_type: str,
) -> None:
    """Reject unsupported scanner-artifact combinations."""

    applicable = applicable_scanners(
        artifact_type
    )

    if scanner not in applicable:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Scanner '{scanner}' is not applicable "
                f"to artifact type '{artifact_type}'. "
                f"Applicable scanners: "
                f"{', '.join(applicable)}."
            ),
        )


def ground_truth_summary(
    ground_truth_path: Path,
) -> dict[str, Any]:
    """Build a frontend-friendly ground-truth summary."""

    if not ground_truth_path.is_file():
        return {
            "exists": False,
            "misconfigurations": [],
            "ids": [],
            "categories": [],
            "subcategories": [],
            "severities": [],
        }

    data = read_yaml(
        ground_truth_path
    )

    items = data.get(
        "misconfigurations",
        [],
    )

    if not isinstance(items, list):
        items = []

    summaries: list[dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        resource = item.get(
            "resource",
            {},
        )

        if not isinstance(resource, dict):
            resource = {}

        summaries.append(
            {
                "id": item.get("id"),
                "category": item.get("category"),
                "subcategory": item.get("subcategory"),
                "severity": item.get("severity"),
                "field_path": item.get("field_path"),
                "bad_value": item.get("bad_value"),
                "expected_secure_value": item.get(
                    "expected_secure_value"
                ),
                "resource": resource,
            }
        )

    def unique_values(
        field_name: str,
    ) -> list[str]:
        values: list[str] = []

        for item in summaries:
            value = item.get(
                field_name
            )

            if value is None:
                continue

            text = str(value)

            if text not in values:
                values.append(text)

        return values

    return {
        "exists": True,
        "case_id": data.get("case_id"),
        "artifact_type": data.get(
            "artifact_type"
        ),
        "misconfigurations": summaries,
        "ids": unique_values("id"),
        "categories": unique_values(
            "category"
        ),
        "subcategories": unique_values(
            "subcategory"
        ),
        "severities": unique_values(
            "severity"
        ),
    }


def validate_case_files(
    case_id: str,
    case_configuration: dict[str, Any],
    artifact_type: str,
) -> tuple[list[str], list[str]]:
    """
    Return case validation errors and warnings.

    This is deliberately read-only. It does not modify the
    corpus or configuration.
    """

    errors: list[str] = []
    warnings: list[str] = []

    try:
        artifact = resolve_project_path(
            case_configuration.get(
                "artifact_path"
            ),
            (
                f"cases.{case_id}."
                "artifact_path"
            ),
        )

    except HTTPException as error:
        errors.append(
            str(error.detail)
        )

        artifact = None

    try:
        ground_truth = resolve_project_path(
            case_configuration.get(
                "ground_truth_path"
            ),
            (
                f"cases.{case_id}."
                "ground_truth_path"
            ),
        )

    except HTTPException as error:
        errors.append(
            str(error.detail)
        )

        ground_truth = None

    if artifact is not None:
        if artifact_type in {
            "kubernetes_yaml",
            "dockerfile",
        }:
            if not artifact.is_file():
                errors.append(
                    "Artifact file does not exist: "
                    f"{relative_path(artifact)}"
                )

        elif artifact_type == "helm_chart":
            if not artifact.is_dir():
                errors.append(
                    "Helm chart directory does not exist: "
                    f"{relative_path(artifact)}"
                )

            else:
                if not (
                    artifact / "Chart.yaml"
                ).is_file():
                    errors.append(
                        "Helm chart is missing Chart.yaml."
                    )

                if not (
                    artifact / "templates"
                ).is_dir():
                    errors.append(
                        "Helm chart is missing templates/."
                    )

                if not (
                    artifact / "values.yaml"
                ).is_file():
                    warnings.append(
                        "Helm chart does not contain values.yaml."
                    )

    if (
        ground_truth is not None
        and not ground_truth.is_file()
    ):
        errors.append(
            "Ground-truth file does not exist: "
            f"{relative_path(ground_truth)}"
        )

    mappings = case_configuration.get(
        "rule_mappings"
    )

    if not isinstance(mappings, dict):
        errors.append(
            "Case does not contain valid rule_mappings."
        )

    return errors, warnings


def build_case_record(
    case_id: str,
    case_configuration: dict[str, Any],
) -> dict[str, Any]:
    """Build one case record for the API."""

    artifact_type = normalise_artifact_type(
        case_configuration.get(
            "artifact_type"
        )
    )

    settings = ARTIFACT_SETTINGS[
        artifact_type
    ]

    artifact_path = resolve_project_path(
        case_configuration.get(
            "artifact_path"
        ),
        f"cases.{case_id}.artifact_path",
    )

    ground_truth_path = resolve_project_path(
        case_configuration.get(
            "ground_truth_path"
        ),
        f"cases.{case_id}.ground_truth_path",
    )

    errors, warnings = validate_case_files(
        case_id=case_id,
        case_configuration=case_configuration,
        artifact_type=artifact_type,
    )

    truth = ground_truth_summary(
        ground_truth_path
    )

    if artifact_type == "helm_chart":
        artifact_name = "Helm chart"

        artifact_contents = {
            "chart_yaml": (
                artifact_path / "Chart.yaml"
            ).is_file(),
            "values_yaml": (
                artifact_path / "values.yaml"
            ).is_file(),
            "templates_directory": (
                artifact_path / "templates"
            ).is_dir(),
        }

    else:
        artifact_name = artifact_path.name

        artifact_contents = None

    mappings = case_configuration.get(
        "rule_mappings",
        {},
    )

    return {
        "case_id": case_id,
        "artifact_type": artifact_type,
        "artifact_label": settings["label"],
        "artifact_name": artifact_name,
        "artifact_path": relative_path(
            artifact_path
        ),
        "artifact_contents": artifact_contents,
        "ground_truth_name": (
            ground_truth_path.name
        ),
        "ground_truth_path": relative_path(
            ground_truth_path
        ),
        "ground_truth": truth,
        "ground_truth_ids": truth["ids"],
        "categories": truth["categories"],
        "subcategories": truth[
            "subcategories"
        ],
        "severities": truth["severities"],
        "applicable_scanners": list(
            applicable_scanners(
                artifact_type
            )
        ),
        "rule_mappings": mappings,
        "validation_status": (
            "valid"
            if not errors
            else "invalid"
        ),
        "validation_errors": errors,
        "validation_warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Output and metric paths
# ---------------------------------------------------------------------------

def result_root(
    artifact_type: str,
    stage: str,
) -> Path:
    """Return the correct output root for a stage."""

    if stage == "raw":
        return (
            PROJECT_ROOT
            / "results"
            / "raw"
        )

    settings = ARTIFACT_SETTINGS[
        artifact_type
    ]

    root_key = {
        "normalised": "normalised_root",
        "matched": "matched_root",
        "metrics": "metrics_root",
    }.get(stage)

    if root_key is None:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported output stage: {stage}"
            ),
        )

    return (
        PROJECT_ROOT
        / settings[root_key]
    )


def output_path(
    stage: str,
    scanner: str,
    case_id: str,
    artifact_type: str,
) -> Path:
    """Return one scanner result path."""

    suffixes = {
        "raw": ".json",
        "normalised": ".normalised.json",
        "matched": ".matched.json",
        "metrics": ".metrics.json",
    }

    suffix = suffixes.get(stage)

    if suffix is None:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported output stage: {stage}"
            ),
        )

    return (
        result_root(
            artifact_type,
            stage,
        )
        / scanner
        / f"{case_id}{suffix}"
    )


def standard_metrics(
    scanner: str,
    case_id: str,
    artifact_type: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    """Convert a generated metrics file into one API schema."""

    nested = (
        data.get("data")
        if isinstance(
            data.get("data"),
            dict,
        )
        else {}
    )

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

    def count(
        long_name: str,
        short_name: str | None = None,
    ) -> int:
        value = counts.get(long_name)

        if value is None and short_name:
            value = counts.get(short_name)

        if value is None:
            value = data.get(long_name)

        try:
            return int(value or 0)

        except (
            TypeError,
            ValueError,
        ):
            return 0

    return {
        "scanner": scanner,
        "case_id": data.get(
            "case_id",
            nested.get(
                "case_id",
                case_id,
            ),
        ),
        "artifact_type": artifact_type,
        "artifact_label": (
            ARTIFACT_SETTINGS[
                artifact_type
            ]["label"]
        ),
        "applicable": True,
        "matching_mode": data.get(
            "matching_mode",
            nested.get(
                "matching_mode"
            ),
        ),
        "counts": {
            "true_positive_count": count(
                "true_positive_count",
                "tp",
            ),
            "false_positive_count": count(
                "false_positive_count",
                "fp",
            ),
            "false_negative_count": count(
                "false_negative_count",
                "fn",
            ),
            "unlabelled_extra_findings_count": count(
                "unlabelled_extra_findings_count",
                "unlabelled_extra_count",
            ),
            "duplicate_match_count": count(
                "duplicate_match_count"
            ),
            "ambiguous_match_count": count(
                "ambiguous_match_count"
            ),
        },
        "metrics": {
            "precision": metrics.get(
                "precision"
            ),
            "recall": metrics.get(
                "recall"
            ),
            "f1_score": metrics.get(
                "f1_score",
                metrics.get("f1"),
            ),
        },
    }


# ---------------------------------------------------------------------------
# Pipeline processing
# ---------------------------------------------------------------------------

def pipeline_script(
    artifact_type: str,
) -> Path:
    """Return the correct runner for an artifact type."""

    script_name = ARTIFACT_SETTINGS[
        artifact_type
    ]["runner"]

    script_path = (
        PROJECT_ROOT
        / "scripts"
        / script_name
    )

    if not script_path.is_file():
        raise HTTPException(
            status_code=500,
            detail=(
                "Pipeline runner not found: "
                f"{relative_path(script_path)}"
            ),
        )

    return script_path


def run_process(
    command: list[str],
    timeout_seconds: int = 600,
) -> tuple[int, str]:
    """Execute a pipeline command and capture its output."""

    try:
        completed = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )

    except subprocess.TimeoutExpired as error:
        output_parts = []

        if error.stdout:
            output_parts.append(
                str(error.stdout)
            )

        if error.stderr:
            output_parts.append(
                str(error.stderr)
            )

        output_parts.append(
            "Pipeline timed out."
        )

        return (
            124,
            "\n".join(output_parts),
        )

    except OSError as error:
        return (
            1,
            f"Could not start pipeline: {error}",
        )

    output = "\n".join(
        value.strip()
        for value in (
            completed.stdout,
            completed.stderr,
        )
        if value and value.strip()
    )

    return (
        completed.returncode,
        output,
    )


def process_one_scanner(
    case_id: str,
    artifact_type: str,
    scanner: str,
    matching_mode: str,
) -> dict[str, Any]:
    """Run the correct analysis pipeline for one scanner."""

    script = pipeline_script(
        artifact_type
    )

    command = [
        sys.executable,
        str(script),
        "--case",
        case_id,
        "--scanners",
        scanner,
        "--matching-mode",
        matching_mode,
    ]

    return_code, console_output = (
        run_process(command)
    )

    metrics_file = output_path(
        stage="metrics",
        scanner=scanner,
        case_id=case_id,
        artifact_type=artifact_type,
    )

    metrics_data = None

    if metrics_file.is_file():
        raw_metrics = read_json(
            metrics_file
        )

        if isinstance(raw_metrics, dict):
            metrics_data = standard_metrics(
                scanner=scanner,
                case_id=case_id,
                artifact_type=artifact_type,
                data=raw_metrics,
            )

            metrics_data["updated_at"] = (
                modified_time(
                    metrics_file
                )
            )

    if return_code == 0:
        status = "completed"
        error_message = None

    else:
        status = "failed"
        error_message = (
            f"Pipeline exited with code "
            f"{return_code}."
        )

    return {
        "scanner": scanner,
        "case_id": case_id,
        "artifact_type": artifact_type,
        "status": status,
        "return_code": return_code,
        "command": command,
        "console_output": console_output,
        "error": error_message,
        "metrics": metrics_data,
    }


def process_request(
    request: ProcessRequest,
) -> dict[str, Any]:
    """Process one benchmark request."""

    case_configuration, artifact_type = (
        get_case_configuration(
            request.case_id
        )
    )

    errors, warnings = validate_case_files(
        case_id=request.case_id,
        case_configuration=case_configuration,
        artifact_type=artifact_type,
    )

    if errors:
        raise HTTPException(
            status_code=400,
            detail={
                "message": (
                    "The benchmark case is invalid."
                ),
                "errors": errors,
                "warnings": warnings,
            },
        )

    applicable = applicable_scanners(
        artifact_type
    )

    selected = (
        list(request.scanners)
        if request.scanners
        else list(applicable)
    )

    selected = list(
        dict.fromkeys(selected)
    )

    invalid_scanners = [
        scanner
        for scanner in selected
        if scanner not in applicable
    ]

    if invalid_scanners:
        raise HTTPException(
            status_code=400,
            detail={
                "message": (
                    "One or more scanners are not "
                    "applicable to this case."
                ),
                "case_id": request.case_id,
                "artifact_type": artifact_type,
                "invalid_scanners": invalid_scanners,
                "applicable_scanners": list(
                    applicable
                ),
            },
        )

    started_at = utc_now()

    results = [
        process_one_scanner(
            case_id=request.case_id,
            artifact_type=artifact_type,
            scanner=scanner,
            matching_mode=(
                request.matching_mode
            ),
        )
        for scanner in selected
    ]

    completed_count = sum(
        result["status"] == "completed"
        for result in results
    )

    failed_count = sum(
        result["status"] == "failed"
        for result in results
    )

    return {
        "operation": "analysis_pipeline",
        "case_id": request.case_id,
        "artifact_type": artifact_type,
        "artifact_label": (
            ARTIFACT_SETTINGS[
                artifact_type
            ]["label"]
        ),
        "matching_mode": (
            request.matching_mode
        ),
        "started_at": started_at,
        "completed_at": utc_now(),
        "selected_scanners": selected,
        "applicable_scanners": list(
            applicable
        ),
        "completed_count": completed_count,
        "failed_count": failed_count,
        "results": results,
    }


# ---------------------------------------------------------------------------
# Report helpers
# ---------------------------------------------------------------------------

def encode_report_id(
    root_key: str,
    relative_report_path: str,
) -> str:
    """Create a URL-safe report identifier."""

    payload = json.dumps(
        {
            "root": root_key,
            "path": relative_report_path,
        },
        separators=(",", ":"),
    ).encode("utf-8")

    return base64.urlsafe_b64encode(
        payload
    ).decode("ascii").rstrip("=")


def decode_report_id(
    report_id: str,
) -> tuple[str, str]:
    """Decode a report identifier."""

    padding = "=" * (
        -len(report_id) % 4
    )

    try:
        payload = base64.urlsafe_b64decode(
            report_id + padding
        )

        data = json.loads(
            payload.decode("utf-8")
        )

    except (
        ValueError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as error:
        raise HTTPException(
            status_code=400,
            detail="Invalid report identifier.",
        ) from error

    root_key = data.get("root")
    report_path = data.get("path")

    if (
        root_key not in REPORT_ROOTS
        or not isinstance(
            report_path,
            str,
        )
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid report identifier.",
        )

    return root_key, report_path


def safe_report_path(
    root_key: str,
    relative_report_path: str,
) -> Path:
    """Resolve a report path safely."""

    root = REPORT_ROOTS[
        root_key
    ].resolve()

    path = (
        root / relative_report_path
    ).resolve()

    try:
        path.relative_to(root)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail="Invalid report path.",
        ) from error

    if path.suffix.lower() != ".md":
        raise HTTPException(
            status_code=400,
            detail=(
                "Only Markdown reports can be opened."
            ),
        )

    return path


def report_records() -> list[dict[str, Any]]:
    """Return reports from every artifact-specific root."""

    records: list[dict[str, Any]] = []

    for root_key, root in REPORT_ROOTS.items():
        if not root.is_dir():
            continue

        for path in root.rglob("*.md"):
            if not path.is_file():
                continue

            relative = str(
                path.relative_to(root)
            ).replace("\\", "/")

            records.append(
                {
                    "id": encode_report_id(
                        root_key,
                        relative,
                    ),
                    "name": path.name,
                    "relative_path": relative,
                    "report_group": root_key,
                    "artifact_type": (
                        None
                        if root_key == "comparison"
                        else root_key
                    ),
                    "artifact_label": (
                        "Combined comparison"
                        if root_key == "comparison"
                        else ARTIFACT_SETTINGS[
                            root_key
                        ]["label"]
                    ),
                    "modified_at": modified_time(
                        path
                    ),
                    "size_bytes": (
                        path.stat().st_size
                    ),
                }
            )

    records.sort(
        key=lambda item: item[
            "modified_at"
        ],
        reverse=True,
    )

    return records


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health() -> dict[str, Any]:
    """Return API and project health information."""

    configuration_exists = (
        CONFIG_PATH.is_file()
    )

    comparison_path = (
        PROJECT_ROOT
        / "results"
        / "comparison"
        / "benchmark-comparison.json"
    )

    return {
        "status": "online",
        "project": "Scanner Benchmark API",
        "api_version": "2.0.0",
        "time": utc_now(),
        "configuration_exists": (
            configuration_exists
        ),
        "comparison_exists": (
            comparison_path.is_file()
        ),
        "supported_artifact_types": list(
            ARTIFACT_SETTINGS.keys()
        ),
        "supported_scanners": list(
            SCANNERS
        ),
    }


@app.get("/api/settings")
def settings() -> dict[str, Any]:
    """Return frontend-safe project settings."""

    artifact_paths: dict[str, Any] = {}

    for (
        artifact_type,
        artifact_settings,
    ) in ARTIFACT_SETTINGS.items():

        artifact_paths[
            artifact_type
        ] = {
            "label": artifact_settings[
                "label"
            ],
            "runner": (
                "scripts/"
                + artifact_settings[
                    "runner"
                ]
            ),
            "applicable_scanners": list(
                artifact_settings[
                    "applicable_scanners"
                ]
            ),
            "normalised_root": (
                artifact_settings[
                    "normalised_root"
                ]
            ),
            "matched_root": (
                artifact_settings[
                    "matched_root"
                ]
            ),
            "metrics_root": (
                artifact_settings[
                    "metrics_root"
                ]
            ),
            "reports_root": (
                artifact_settings[
                    "reports_root"
                ]
            ),
        }

    return {
        "project_root": str(
            PROJECT_ROOT
        ),
        "configuration": relative_path(
            CONFIG_PATH
        ),
        "raw_root": "results/raw",
        "comparison_root": (
            "results/comparison"
        ),
        "artifact_types": artifact_paths,
    }


@app.get("/api/cases")
def cases() -> dict[str, Any]:
    """List all configured benchmark cases."""

    configuration = (
        load_benchmark_config()
    )

    case_mapping = configuration[
        "cases"
    ]

    records = [
        build_case_record(
            case_id,
            case_configuration,
        )
        for (
            case_id,
            case_configuration,
        ) in case_mapping.items()
        if isinstance(
            case_configuration,
            dict,
        )
    ]

    artifact_order = {
        "kubernetes_yaml": 0,
        "dockerfile": 1,
        "helm_chart": 2,
    }

    records.sort(
        key=lambda item: (
            artifact_order.get(
                item["artifact_type"],
                99,
            ),
            item["case_id"],
        )
    )

    family_counts = {
        artifact_type: sum(
            record["artifact_type"]
            == artifact_type
            for record in records
        )
        for artifact_type
        in ARTIFACT_SETTINGS
    }

    return {
        "case_count": len(records),
        "family_counts": family_counts,
        "cases": records,
    }


@app.get("/api/cases/{case_id}")
def case_detail(
    case_id: str,
) -> dict[str, Any]:
    """Return one configured benchmark case."""

    case_configuration, _ = (
        get_case_configuration(
            case_id
        )
    )

    return build_case_record(
        case_id,
        case_configuration,
    )


@app.get("/api/metrics/{scanner}")
def metric_result(
    scanner: str,
    case_id: str = Query(
        ...,
        min_length=1,
    ),
) -> dict[str, Any]:
    """Return one scanner-case metrics result."""

    scanner = validate_scanner(
        scanner
    )

    _, artifact_type = (
        get_case_configuration(
            case_id
        )
    )

    ensure_scanner_applicable(
        scanner,
        artifact_type,
    )

    path = output_path(
        stage="metrics",
        scanner=scanner,
        case_id=case_id,
        artifact_type=artifact_type,
    )

    data = read_json(path)

    if not isinstance(data, dict):
        raise HTTPException(
            status_code=500,
            detail=(
                "Metrics output must contain "
                "a JSON object."
            ),
        )

    result = standard_metrics(
        scanner=scanner,
        case_id=case_id,
        artifact_type=artifact_type,
        data=data,
    )

    result["updated_at"] = (
        modified_time(path)
    )

    result["path"] = relative_path(
        path
    )

    return result


@app.get("/api/cases/{case_id}/metrics")
def case_metrics(
    case_id: str,
) -> dict[str, Any]:
    """
    Return all scanner statuses and available metrics
    for one case.
    """

    _, artifact_type = (
        get_case_configuration(
            case_id
        )
    )

    applicable = applicable_scanners(
        artifact_type
    )

    rows: list[dict[str, Any]] = []

    for scanner in SCANNERS:
        if scanner not in applicable:
            rows.append(
                {
                    "scanner": scanner,
                    "case_id": case_id,
                    "artifact_type": (
                        artifact_type
                    ),
                    "applicable": False,
                    "status": (
                        "not_applicable"
                    ),
                    "counts": None,
                    "metrics": None,
                }
            )

            continue

        path = output_path(
            stage="metrics",
            scanner=scanner,
            case_id=case_id,
            artifact_type=artifact_type,
        )

        if not path.is_file():
            rows.append(
                {
                    "scanner": scanner,
                    "case_id": case_id,
                    "artifact_type": (
                        artifact_type
                    ),
                    "applicable": True,
                    "status": "missing",
                    "counts": None,
                    "metrics": None,
                    "path": relative_path(
                        path
                    ),
                }
            )

            continue

        data = read_json(path)

        if not isinstance(data, dict):
            rows.append(
                {
                    "scanner": scanner,
                    "case_id": case_id,
                    "artifact_type": (
                        artifact_type
                    ),
                    "applicable": True,
                    "status": "invalid",
                    "counts": None,
                    "metrics": None,
                    "path": relative_path(
                        path
                    ),
                }
            )

            continue

        row = standard_metrics(
            scanner=scanner,
            case_id=case_id,
            artifact_type=artifact_type,
            data=data,
        )

        row["status"] = "available"
        row["updated_at"] = (
            modified_time(path)
        )
        row["path"] = relative_path(
            path
        )

        rows.append(row)

    return {
        "case_id": case_id,
        "artifact_type": artifact_type,
        "artifact_label": (
            ARTIFACT_SETTINGS[
                artifact_type
            ]["label"]
        ),
        "applicable_scanners": list(
            applicable
        ),
        "results": rows,
    }


@app.get(
    "/api/outputs/{stage}/{scanner}"
)
def outputs(
    stage: str,
    scanner: str,
    case_id: str = Query(
        ...,
        min_length=1,
    ),
) -> dict[str, Any]:
    """Return one pipeline output file."""

    stage = stage.strip().lower()
    scanner = validate_scanner(
        scanner
    )

    if stage not in OUTPUT_STAGES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported stage: {stage}"
            ),
        )

    _, artifact_type = (
        get_case_configuration(
            case_id
        )
    )

    ensure_scanner_applicable(
        scanner,
        artifact_type,
    )

    path = output_path(
        stage=stage,
        scanner=scanner,
        case_id=case_id,
        artifact_type=artifact_type,
    )

    return {
        "stage": stage,
        "scanner": scanner,
        "case_id": case_id,
        "artifact_type": artifact_type,
        "artifact_label": (
            ARTIFACT_SETTINGS[
                artifact_type
            ]["label"]
        ),
        "path": relative_path(path),
        "updated_at": (
            modified_time(path)
            if path.is_file()
            else None
        ),
        "data": read_json(path),
    }


@app.get("/api/comparison")
def comparison() -> dict[str, Any]:
    """Return the combined comparison report JSON."""

    path = (
        PROJECT_ROOT
        / "results"
        / "comparison"
        / "benchmark-comparison.json"
    )

    data = read_json(path)

    if not isinstance(data, dict):
        raise HTTPException(
            status_code=500,
            detail=(
                "Comparison report must contain "
                "a JSON object."
            ),
        )

    data["comparison_path"] = (
        relative_path(path)
    )

    data["updated_at"] = (
        modified_time(path)
    )

    return data


@app.get(
    "/api/comparison/markdown",
    response_class=PlainTextResponse,
)
def comparison_markdown() -> str:
    """Return the combined comparison Markdown report."""

    path = (
        PROJECT_ROOT
        / "results"
        / "comparison"
        / "benchmark-comparison.md"
    )

    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail=(
                "Comparison Markdown report has "
                "not been generated."
            ),
        )

    return path.read_text(
        encoding="utf-8-sig"
    )


@app.post("/api/comparison/generate")
def generate_comparison() -> dict[str, Any]:
    """Generate or refresh the comparison report."""

    script = (
        PROJECT_ROOT
        / "scripts"
        / "generate_comparison_report.py"
    )

    if not script.is_file():
        raise HTTPException(
            status_code=500,
            detail=(
                "Comparison script not found: "
                f"{relative_path(script)}"
            ),
        )

    command = [
        sys.executable,
        str(script),
    ]

    return_code, console_output = (
        run_process(
            command,
            timeout_seconds=300,
        )
    )

    if return_code != 0:
        raise HTTPException(
            status_code=500,
            detail={
                "message": (
                    "Comparison report generation failed."
                ),
                "return_code": return_code,
                "console_output": console_output,
            },
        )

    comparison_path = (
        PROJECT_ROOT
        / "results"
        / "comparison"
        / "benchmark-comparison.json"
    )

    data = read_json(
        comparison_path
    )

    return {
        "status": "completed",
        "return_code": return_code,
        "console_output": console_output,
        "comparison": data,
    }


@app.get("/api/reports")
def reports() -> dict[str, Any]:
    """List every generated Markdown report."""

    records = report_records()

    return {
        "report_count": len(records),
        "reports": records,
    }


@app.get(
    "/api/reports/{report_id}",
    response_class=PlainTextResponse,
)
def report(
    report_id: str,
) -> str:
    """Open a report by its safe API identifier."""

    root_key, report_path = (
        decode_report_id(
            report_id
        )
    )

    path = safe_report_path(
        root_key,
        report_path,
    )

    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Report not found.",
        )

    return path.read_text(
        encoding="utf-8-sig"
    )


@app.post("/api/process")
def process(
    request: ProcessRequest,
) -> dict[str, Any]:
    """
    Process existing raw scanner outputs using the correct
    artifact-specific benchmark runner.
    """

    return process_request(
        request
    )


@app.post("/api/run")
def legacy_run(
    request: ProcessRequest,
) -> dict[str, Any]:
    """
    Compatibility alias for the existing frontend.

    This endpoint processes existing raw outputs. It does not
    execute the scanner CLI tools themselves.
    """

    return process_request(
        request
    )


# ---------------------------------------------------------------------------
# Frontend hosting
# ---------------------------------------------------------------------------

if FRONTEND_DIR.is_dir():
    app.mount(
        "/",
        StaticFiles(
            directory=FRONTEND_DIR,
            html=True,
        ),
        name="frontend",
    )