"""Scan and process benchmark cases 003 through 010."""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config_loader import PROJECT_ROOT, load_benchmark_config


CASE_MINIMUM = 3
CASE_MAXIMUM = 10

ARTIFACT_ORDER = {
    "kubernetes_yaml": 0,
    "dockerfile": 1,
    "helm_chart": 2,
}

SCANNERS_BY_ARTIFACT = {
    "kubernetes_yaml": ("checkov", "trivy", "kubescape"),
    "dockerfile": ("checkov", "trivy"),
    "helm_chart": ("checkov", "trivy", "kubescape"),
}

RUNNERS_BY_ARTIFACT = {
    "kubernetes_yaml": "run_benchmark.py",
    "dockerfile": "run_dockerfile_benchmark.py",
    "helm_chart": "run_helm_benchmark.py",
}


class BatchError(Exception):
    """Raised when the batch configuration is invalid."""


@dataclass(frozen=True)
class CasePlan:
    """One configured case selected for the batch."""

    case_id: str
    case_number: int
    artifact_type: str
    artifact_path: Path


def parse_arguments() -> argparse.Namespace:
    """Read batch options."""

    parser = argparse.ArgumentParser(
        description=(
            "Generate raw scanner JSON and run the strict benchmark "
            "pipeline for Kubernetes, Dockerfile and Helm cases 003-010."
        )
    )
    parser.add_argument(
        "--scanners",
        nargs="+",
        choices=("checkov", "trivy", "kubescape"),
        help="Run only the selected scanners. The default is all scanners.",
    )
    parser.add_argument(
        "--mode",
        choices=("all", "scan", "process"),
        default="all",
        help=(
            "Run scanners and processing, scanners only, or processing "
            "only. The default is all."
        ),
    )
    parser.add_argument(
        "--reuse-raw",
        action="store_true",
        help="Keep valid existing raw JSON instead of scanning it again.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without running scanners or pipelines.",
    )
    return parser.parse_args()


def configured_case_number(case_id: str, artifact_type: str) -> int | None:
    """Return the numeric portion of a case ID for its artifact family."""

    prefixes = {
        "kubernetes_yaml": "case-",
        "dockerfile": "case-docker-",
        "helm_chart": "case-helm-",
    }
    prefix = prefixes.get(artifact_type)
    if prefix is None or not case_id.startswith(prefix):
        return None

    number_text = case_id[len(prefix):].split("-", 1)[0]
    if not number_text.isdigit():
        return None

    return int(number_text)


def select_case_plans(configuration: dict[str, Any]) -> list[CasePlan]:
    """Select configured cases 003 through 010 from all artifact families."""

    case_mapping = configuration.get("cases")
    if not isinstance(case_mapping, dict):
        raise BatchError("benchmark_config.yaml has no valid cases mapping.")

    plans: list[CasePlan] = []
    for case_id, case_configuration in case_mapping.items():
        if not isinstance(case_id, str) or not isinstance(case_configuration, dict):
            continue

        artifact_type = case_configuration.get("artifact_type")
        if artifact_type not in SCANNERS_BY_ARTIFACT:
            continue

        case_number = configured_case_number(case_id, artifact_type)
        if case_number is None or not CASE_MINIMUM <= case_number <= CASE_MAXIMUM:
            continue

        artifact_value = case_configuration.get("artifact_path")
        if not isinstance(artifact_value, str) or not artifact_value.strip():
            raise BatchError(f"{case_id} has no valid artifact_path.")

        artifact_path = (PROJECT_ROOT / artifact_value).resolve()
        try:
            artifact_path.relative_to(PROJECT_ROOT)
        except ValueError as error:
            raise BatchError(f"{case_id} artifact_path leaves the project.") from error

        if not artifact_path.exists():
            raise BatchError(f"Artifact does not exist for {case_id}: {artifact_path}")

        plans.append(
            CasePlan(
                case_id=case_id,
                case_number=case_number,
                artifact_type=artifact_type,
                artifact_path=artifact_path,
            )
        )

    plans.sort(
        key=lambda plan: (
            ARTIFACT_ORDER[plan.artifact_type],
            plan.case_number,
            plan.case_id,
        )
    )
    return plans


def relative(path: Path) -> str:
    """Return a project-relative path for commands and messages."""

    return str(path.relative_to(PROJECT_ROOT))


def raw_output_path(scanner: str, case_id: str) -> Path:
    """Return the raw JSON path expected by the benchmark pipeline."""

    return PROJECT_ROOT / "results" / "raw" / scanner / f"{case_id}.json"


def scanner_command(plan: CasePlan, scanner: str, output_path: Path) -> list[str]:
    """Build the scanner command for one case."""

    artifact = relative(plan.artifact_path)
    output = relative(output_path)

    if scanner == "checkov":
        input_flag = "--directory" if plan.artifact_type == "helm_chart" else "--file"
        framework = {
            "kubernetes_yaml": "kubernetes",
            "dockerfile": "dockerfile",
            "helm_chart": "helm",
        }[plan.artifact_type]
        return [
            "checkov",
            input_flag,
            artifact,
            "--framework",
            framework,
            "--output",
            "json",
        ]

    if scanner == "trivy":
        return [
            "trivy",
            "config",
            "--disable-telemetry",
            "--format",
            "json",
            "--output",
            output,
            artifact,
        ]

    if scanner == "kubescape":
        return [
            "kubescape",
            "scan",
            artifact,
            "--format",
            "json",
            "--output",
            output,
        ]

    raise BatchError(f"Unsupported scanner: {scanner}")


def load_valid_raw(scanner: str, path: Path) -> tuple[bool, str | None]:
    """Validate the top-level raw JSON shape expected for one scanner."""

    if not path.is_file() or path.stat().st_size == 0:
        return False, "file is missing or empty"

    try:
        with path.open("r", encoding="utf-8-sig") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        return False, str(error)

    if scanner == "checkov":
        blocks = data if isinstance(data, list) else [data]
        valid = bool(blocks) and all(isinstance(block, dict) for block in blocks)
        if valid and any(isinstance(block.get("results"), dict) for block in blocks):
            return True, None
        return False, "Checkov JSON has no results object"

    if scanner == "trivy":
        if isinstance(data, dict) and isinstance(data.get("Results"), list):
            return True, None
        return False, "Trivy JSON has no Results list"

    if scanner == "kubescape":
        if isinstance(data, dict) and isinstance(data.get("summaryDetails"), dict):
            return True, None
        return False, "Kubescape JSON has no summaryDetails object"

    return False, f"unsupported scanner {scanner}"


def scan_case(plan: CasePlan, scanner: str, dry_run: bool) -> bool:
    """Generate and validate one raw scanner JSON file."""

    destination = raw_output_path(scanner, plan.case_id)
    temporary = destination.with_name(f".{destination.stem}.tmp.json")
    command = scanner_command(plan, scanner, temporary)

    if dry_run:
        rendered = shlex.join(command)
        if scanner == "checkov":
            rendered += f" > {shlex.quote(relative(temporary))}"
        print(f"  SCAN {rendered}")
        return True

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary.unlink(missing_ok=True)

    print(f"  Scanning with {scanner}...")
    try:
        if scanner == "checkov":
            with temporary.open("w", encoding="utf-8") as output_file:
                completed = subprocess.run(
                    command,
                    cwd=PROJECT_ROOT,
                    stdout=output_file,
                    check=False,
                )
        else:
            completed = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    except OSError as error:
        print(f"  FAILED to start {scanner}: {error}")
        temporary.unlink(missing_ok=True)
        return False

    valid, reason = load_valid_raw(scanner, temporary)
    if not valid:
        print(
            f"  FAILED {scanner} scan (exit {completed.returncode}): "
            f"{reason}"
        )
        temporary.unlink(missing_ok=True)
        return False

    temporary.replace(destination)
    return_code_note = (
        f"; scanner exit {completed.returncode}"
        if completed.returncode != 0
        else ""
    )
    print(f"  Saved {relative(destination)}{return_code_note}")
    return True


def process_case(plan: CasePlan, scanner: str, dry_run: bool) -> bool:
    """Run the strict benchmark pipeline for one scanner-case pair."""

    runner = PROJECT_ROOT / "scripts" / RUNNERS_BY_ARTIFACT[plan.artifact_type]
    command = [
        sys.executable,
        str(runner),
        "--case",
        plan.case_id,
        "--scanners",
        scanner,
        "--matching-mode",
        "strict",
    ]

    if dry_run:
        print(f"  PROCESS {shlex.join(command)}")
        return True

    print(f"  Processing {scanner} output...")
    completed = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    return completed.returncode == 0


def save_scanner_versions(scanners: tuple[str, ...], dry_run: bool) -> list[str]:
    """Record the installed scanner versions beside the raw outputs."""

    failures: list[str] = []
    commands = {
        "checkov": ["checkov", "--version"],
        "trivy": ["trivy", "version"],
        "kubescape": ["kubescape", "version"],
    }

    for scanner in scanners:
        command = commands[scanner]
        version_path = PROJECT_ROOT / "results" / "raw" / scanner / f"{scanner}-version.txt"
        if dry_run:
            print(f"VERSION {shlex.join(command)} > {relative(version_path)}")
            continue

        completed = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        version_text = completed.stdout.strip() or completed.stderr.strip()
        if completed.returncode != 0 or not version_text:
            failures.append(f"{scanner}: could not read version")
            continue

        version_path.parent.mkdir(parents=True, exist_ok=True)
        version_path.write_text(version_text + "\n", encoding="utf-8")

    return failures


def ensure_tools_available(scanners: tuple[str, ...], plans: list[CasePlan]) -> None:
    """Fail early when a required scanner or supporting tool is unavailable."""

    missing = [
        scanner
        for scanner in scanners
        if shutil.which(scanner) is None
    ]
    if missing:
        raise BatchError(
            "Missing scanner executables: "
            + ", ".join(missing)
            + ". Install them with: brew install checkov trivy kubescape"
        )

    checkov_needs_helm = "checkov" in scanners and any(
        plan.artifact_type == "helm_chart" for plan in plans
    )
    if checkov_needs_helm and shutil.which("helm") is None:
        raise BatchError(
            "Checkov Helm scans require the Helm executable. "
            "Install it with: brew install helm"
        )


def run() -> int:
    """Run every selected scanner-case operation and print a summary."""

    arguments = parse_arguments()
    configuration = load_benchmark_config()
    plans = select_case_plans(configuration)
    if not plans:
        raise BatchError("No configured cases numbered 003 through 010 were found.")

    scanners = tuple(arguments.scanners or ("checkov", "trivy", "kubescape"))

    expected_families = set(SCANNERS_BY_ARTIFACT)
    found_families = {plan.artifact_type for plan in plans}
    missing_families = expected_families - found_families
    if missing_families:
        raise BatchError("Missing configured artifact families: " + ", ".join(sorted(missing_families)))

    if arguments.mode in ("all", "scan") and not arguments.dry_run:
        ensure_tools_available(scanners, plans)

    operations = sum(
        len(set(SCANNERS_BY_ARTIFACT[plan.artifact_type]) & set(scanners))
        for plan in plans
    )
    print(
        f"Selected {len(plans)} cases and {operations} applicable "
        "scanner-case operations."
    )

    failures: list[str] = []
    if arguments.mode in ("all", "scan"):
        failures.extend(save_scanner_versions(scanners, arguments.dry_run))

    for plan in plans:
        print(f"\n[{plan.artifact_type}] {plan.case_id}")
        for scanner in SCANNERS_BY_ARTIFACT[plan.artifact_type]:
            if scanner not in scanners:
                continue
            raw_path = raw_output_path(scanner, plan.case_id)
            raw_valid, _ = load_valid_raw(scanner, raw_path)

            if arguments.mode in ("all", "scan"):
                if arguments.reuse_raw and raw_valid:
                    print(f"  Reusing {relative(raw_path)}")
                    scan_succeeded = True
                else:
                    scan_succeeded = scan_case(plan, scanner, arguments.dry_run)
            else:
                scan_succeeded = arguments.dry_run or raw_valid
                if not scan_succeeded:
                    print(f"  FAILED: valid raw {scanner} JSON is unavailable")

            if not scan_succeeded:
                failures.append(f"{plan.case_id}/{scanner}: scan")
                continue

            if arguments.mode in ("all", "process"):
                if not process_case(plan, scanner, arguments.dry_run):
                    failures.append(f"{plan.case_id}/{scanner}: processing")

    print("\nBatch summary")
    print(f"Cases: {len(plans)}")
    print(f"Scanner-case operations: {operations}")
    print(f"Failures: {len(failures)}")
    for failure in failures:
        print(f"  - {failure}")

    return 1 if failures else 0


def main() -> int:
    """Application entry point."""

    try:
        return run()
    except (BatchError, KeyError, TypeError, ValueError) as error:
        print(f"Batch failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
