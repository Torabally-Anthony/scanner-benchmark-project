from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config_loader import (
    PROJECT_ROOT,
    ConfigurationError,
    get_case_configuration,
    load_benchmark_config,
)


SUPPORTED_SCANNERS = {
    "checkov",
    "trivy",
}

SUPPORTED_MATCHING_MODES = {
    "review",
    "strict",
}

PIPELINE_STAGES = [
    "Normalisation",
    "Ground-truth matching",
    "Metrics calculation",
    "Report generation",
]


class DockerfilePipelineError(Exception):
    """Raised when the Dockerfile benchmark pipeline cannot run."""


@dataclass
class StageResult:
    """Stores the result of one pipeline stage."""

    scanner: str
    stage: str
    success: bool
    return_code: int
    duration_seconds: float
    command: list[str]
    error_message: str | None = None


def parse_arguments() -> argparse.Namespace:
    """Read command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Run the generic analysis pipeline for a "
            "Dockerfile benchmark case using existing "
            "Checkov and Trivy raw JSON outputs."
        )
    )

    parser.add_argument(
        "--case",
        required=True,
        dest="case_id",
        help="Dockerfile benchmark case ID.",
    )

    parser.add_argument(
        "--scanners",
        nargs="+",
        default=None,
        help=(
            "Dockerfile scanners to process. Supported values "
            "are checkov and trivy. When omitted, both scanners "
            "are processed."
        ),
    )

    parser.add_argument(
        "--matching-mode",
        choices=sorted(SUPPORTED_MATCHING_MODES),
        default=None,
        help=(
            "Matching mode. When omitted, the default from "
            "benchmark_config.yaml is used."
        ),
    )

    parser.add_argument(
        "--normalised-root",
        default="results/normalised_dockerfile",
        help=(
            "Directory where Dockerfile normalised findings "
            "will be saved."
        ),
    )

    parser.add_argument(
        "--matched-root",
        default="results/matched_dockerfile",
        help=(
            "Directory where Dockerfile matched findings "
            "will be saved."
        ),
    )

    parser.add_argument(
        "--metrics-root",
        default="results/metrics_dockerfile",
        help=(
            "Directory where Dockerfile metrics will be saved."
        ),
    )

    parser.add_argument(
        "--reports-root",
        default="results/reports_dockerfile",
        help=(
            "Directory where Dockerfile Markdown reports "
            "will be saved."
        ),
    )

    parser.add_argument(
        "--decimal-places",
        type=int,
        default=4,
        help=(
            "Number of decimal places used when calculating "
            "precision, recall and F1."
        ),
    )

    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help=(
            "Continue with the remaining scanner when one "
            "scanner fails. By default, the pipeline stops "
            "after the first failure."
        ),
    )

    return parser.parse_args()


def clean_text(value: Any) -> str | None:
    """Return a stripped string or None."""

    if not isinstance(value, str):
        return None

    cleaned_value = value.strip()

    return cleaned_value or None


def clean_scanner_name(value: Any) -> str:
    """Clean and validate one Dockerfile scanner name."""

    scanner = clean_text(value)

    if scanner is None:
        raise DockerfilePipelineError(
            f"Invalid scanner value: {value!r}"
        )

    scanner = scanner.lower()

    if scanner not in SUPPORTED_SCANNERS:
        supported = ", ".join(
            sorted(SUPPORTED_SCANNERS)
        )

        raise DockerfilePipelineError(
            f"Scanner '{scanner}' is not supported by the "
            "Dockerfile benchmark runner. Supported scanners: "
            f"{supported}."
        )

    return scanner


def remove_duplicates(
    values: list[str],
) -> list[str]:
    """Remove duplicate values while preserving order."""

    unique_values: list[str] = []
    seen_values: set[str] = set()

    for value in values:
        if value in seen_values:
            continue

        seen_values.add(value)
        unique_values.append(value)

    return unique_values


def resolve_scanners(
    arguments: argparse.Namespace,
) -> list[str]:
    """Resolve the selected Dockerfile scanners."""

    scanner_values = (
        arguments.scanners
        if arguments.scanners
        else [
            "checkov",
            "trivy",
        ]
    )

    scanners = [
        clean_scanner_name(value)
        for value in scanner_values
    ]

    scanners = remove_duplicates(
        scanners
    )

    if not scanners:
        raise DockerfilePipelineError(
            "No Dockerfile scanners were selected."
        )

    return scanners


def resolve_matching_mode(
    arguments: argparse.Namespace,
    configuration: dict[str, Any],
) -> str:
    """Resolve the matching mode from arguments or configuration."""

    if arguments.matching_mode:
        matching_mode = arguments.matching_mode

    else:
        defaults = configuration.get(
            "defaults",
            {},
        )

        if not isinstance(defaults, dict):
            defaults = {}

        matching_mode = defaults.get(
            "matching_mode",
            "review",
        )

    matching_mode = str(
        matching_mode
    ).strip().lower()

    if matching_mode not in SUPPORTED_MATCHING_MODES:
        raise DockerfilePipelineError(
            "Matching mode must be 'review' or 'strict'."
        )

    return matching_mode


def resolve_project_path(
    path_value: Any,
    field_name: str,
) -> Path:
    """
    Resolve a project-relative path and prevent paths
    outside the project.
    """

    clean_path = clean_text(
        path_value
    )

    if clean_path is None:
        raise DockerfilePipelineError(
            f"{field_name} must be a non-empty string."
        )

    path = (
        PROJECT_ROOT
        / clean_path
    ).resolve()

    try:
        path.relative_to(
            PROJECT_ROOT.resolve()
        )

    except ValueError as error:
        raise DockerfilePipelineError(
            f"{field_name} must remain inside the "
            "benchmark project directory."
        ) from error

    return path


def validate_internal_directory(
    directory_value: str,
    field_name: str,
) -> Path:
    """Validate a pipeline output directory."""

    return resolve_project_path(
        path_value=directory_value,
        field_name=field_name,
    )


def validate_dockerfile_case(
    case_id: str,
    configuration: dict[str, Any],
) -> dict[str, Any]:
    """Confirm that the requested case is a Dockerfile case."""

    case_configuration = get_case_configuration(
        configuration,
        case_id,
    )

    artifact_type = clean_text(
        case_configuration.get(
            "artifact_type"
        )
    )

    if artifact_type is None:
        raise DockerfilePipelineError(
            f"Case '{case_id}' does not contain a valid "
            "artifact_type."
        )

    artifact_type = artifact_type.lower()

    if artifact_type != "dockerfile":
        raise DockerfilePipelineError(
            f"Case '{case_id}' has artifact type "
            f"'{artifact_type}'. The Dockerfile benchmark "
            "runner only accepts artifact_type: dockerfile."
        )

    artifact_path = resolve_project_path(
        path_value=case_configuration.get(
            "artifact_path"
        ),
        field_name=(
            f"cases.{case_id}.artifact_path"
        ),
    )

    if not artifact_path.exists():
        raise DockerfilePipelineError(
            "Dockerfile artifact does not exist: "
            f"{artifact_path.relative_to(PROJECT_ROOT)}"
        )

    if not artifact_path.is_file():
        raise DockerfilePipelineError(
            "Dockerfile artifact path is not a file: "
            f"{artifact_path.relative_to(PROJECT_ROOT)}"
        )

    ground_truth_path = resolve_project_path(
        path_value=case_configuration.get(
            "ground_truth_path"
        ),
        field_name=(
            f"cases.{case_id}.ground_truth_path"
        ),
    )

    if not ground_truth_path.exists():
        raise DockerfilePipelineError(
            "Dockerfile ground-truth file does not exist: "
            f"{ground_truth_path.relative_to(PROJECT_ROOT)}"
        )

    if not ground_truth_path.is_file():
        raise DockerfilePipelineError(
            "Dockerfile ground-truth path is not a file: "
            f"{ground_truth_path.relative_to(PROJECT_ROOT)}"
        )

    return case_configuration


def validate_pipeline_scripts() -> None:
    """Confirm that all shared pipeline scripts exist."""

    required_scripts = [
        "normalize_findings.py",
        "match_findings.py",
        "compute_metrics.py",
        "generate_report.py",
    ]

    missing_scripts: list[str] = []

    for script_name in required_scripts:
        script_path = (
            PROJECT_ROOT
            / "scripts"
            / script_name
        )

        if not script_path.exists():
            missing_scripts.append(
                str(
                    script_path.relative_to(
                        PROJECT_ROOT
                    )
                )
            )

    if missing_scripts:
        missing_text = "\n".join(
            f"  - {path}"
            for path in missing_scripts
        )

        raise DockerfilePipelineError(
            "The following shared pipeline scripts "
            f"are missing:\n{missing_text}"
        )


def raw_output_path(
    scanner: str,
    case_id: str,
) -> Path:
    """Return the expected scanner raw-output path."""

    return (
        PROJECT_ROOT
        / "results"
        / "raw"
        / scanner
        / f"{case_id}.json"
    )


def validate_raw_output(
    scanner: str,
    case_id: str,
) -> Path:
    """Confirm that the scanner raw JSON file exists."""

    path = raw_output_path(
        scanner=scanner,
        case_id=case_id,
    )

    if not path.exists():
        raise DockerfilePipelineError(
            f"Raw {scanner} output does not exist: "
            f"{path.relative_to(PROJECT_ROOT)}"
        )

    if not path.is_file():
        raise DockerfilePipelineError(
            f"Raw {scanner} output is not a file: "
            f"{path.relative_to(PROJECT_ROOT)}"
        )

    return path


def format_command(
    command: list[str],
) -> str:
    """Create a readable command string."""

    if os.name == "nt":
        return subprocess.list2cmdline(
            command
        )

    return shlex.join(command)


def print_pipeline_header(
    case_id: str,
    scanners: list[str],
    matching_mode: str,
) -> None:
    """Print the Dockerfile pipeline configuration."""

    separator = "=" * 72

    print()
    print(separator)
    print("Dockerfile benchmark pipeline")
    print(f"Case: {case_id}")
    print(f"Matching mode: {matching_mode}")
    print(
        "Scanners: "
        + ", ".join(scanners)
    )
    print(separator)


def print_stage_header(
    scanner: str,
    stage: str,
    command: list[str],
) -> None:
    """Print information before a stage starts."""

    print()
    print("-" * 72)
    print(
        f"[{scanner}] Starting stage: {stage}"
    )
    print(
        f"[{scanner}] Command: "
        f"{format_command(command)}"
    )
    print("-" * 72)


def run_stage(
    scanner: str,
    stage: str,
    command: list[str],
) -> StageResult:
    """Run one shared pipeline stage."""

    print_stage_header(
        scanner=scanner,
        stage=stage,
        command=command,
    )

    started_at = time.perf_counter()

    environment = os.environ.copy()
    environment["PYTHONUNBUFFERED"] = "1"

    try:
        process = subprocess.Popen(
            command,
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            env=environment,
        )

    except OSError as error:
        duration = (
            time.perf_counter()
            - started_at
        )

        error_message = (
            f"Could not start stage: {error}"
        )

        print(
            f"[{scanner}] {stage}: FAILED"
        )
        print(
            f"[{scanner}] {error_message}"
        )

        return StageResult(
            scanner=scanner,
            stage=stage,
            success=False,
            return_code=1,
            duration_seconds=duration,
            command=command,
            error_message=error_message,
        )

    if process.stdout is not None:
        for line in process.stdout:
            print(
                line,
                end="",
            )

    return_code = process.wait()

    duration = (
        time.perf_counter()
        - started_at
    )

    success = return_code == 0

    status = (
        "PASSED"
        if success
        else "FAILED"
    )

    print()
    print(
        f"[{scanner}] {stage}: {status} "
        f"({duration:.2f} seconds)"
    )

    error_message = None

    if not success:
        error_message = (
            f"Stage returned exit code "
            f"{return_code}."
        )

        print(
            f"[{scanner}] {error_message}"
        )

    return StageResult(
        scanner=scanner,
        stage=stage,
        success=success,
        return_code=return_code,
        duration_seconds=duration,
        command=command,
        error_message=error_message,
    )


def build_pipeline_commands(
    case_id: str,
    scanner: str,
    matching_mode: str,
    normalised_root: str,
    matched_root: str,
    metrics_root: str,
    reports_root: str,
    decimal_places: int,
) -> list[tuple[str, list[str]]]:
    """Build the ordered shared pipeline commands."""

    scripts_directory = (
        PROJECT_ROOT
        / "scripts"
    )

    python_executable = sys.executable

    normalisation_command = [
        python_executable,
        str(
            scripts_directory
            / "normalize_findings.py"
        ),
        "--case",
        case_id,
        "--scanner",
        scanner,
        "--output-root",
        normalised_root,
    ]

    matching_command = [
        python_executable,
        str(
            scripts_directory
            / "match_findings.py"
        ),
        "--case",
        case_id,
        "--scanner",
        scanner,
        "--matching-mode",
        matching_mode,
        "--input-root",
        normalised_root,
        "--output-root",
        matched_root,
    ]

    metrics_command = [
        python_executable,
        str(
            scripts_directory
            / "compute_metrics.py"
        ),
        "--case",
        case_id,
        "--scanner",
        scanner,
        "--input-root",
        matched_root,
        "--output-root",
        metrics_root,
        "--decimal-places",
        str(decimal_places),
    ]

    report_command = [
        python_executable,
        str(
            scripts_directory
            / "generate_report.py"
        ),
        "--case",
        case_id,
        "--scanner",
        scanner,
        "--matched-root",
        matched_root,
        "--metrics-root",
        metrics_root,
        "--output-root",
        reports_root,
    ]

    return [
        (
            "Normalisation",
            normalisation_command,
        ),
        (
            "Ground-truth matching",
            matching_command,
        ),
        (
            "Metrics calculation",
            metrics_command,
        ),
        (
            "Report generation",
            report_command,
        ),
    ]


def run_scanner_pipeline(
    case_id: str,
    scanner: str,
    matching_mode: str,
    arguments: argparse.Namespace,
) -> list[StageResult]:
    """Run every analysis stage for one Dockerfile scanner."""

    validate_raw_output(
        scanner=scanner,
        case_id=case_id,
    )

    commands = build_pipeline_commands(
        case_id=case_id,
        scanner=scanner,
        matching_mode=matching_mode,
        normalised_root=(
            arguments.normalised_root
        ),
        matched_root=(
            arguments.matched_root
        ),
        metrics_root=(
            arguments.metrics_root
        ),
        reports_root=(
            arguments.reports_root
        ),
        decimal_places=(
            arguments.decimal_places
        ),
    )

    results: list[StageResult] = []

    for stage, command in commands:
        result = run_stage(
            scanner=scanner,
            stage=stage,
            command=command,
        )

        results.append(result)

        if not result.success:
            break

    return results


def print_summary(
    case_id: str,
    scanners: list[str],
    results: list[StageResult],
    scanner_errors: dict[str, str],
    total_duration: float,
) -> None:
    """Print the final Dockerfile pipeline summary."""

    print()
    print("=" * 72)
    print("Dockerfile benchmark pipeline summary")
    print("=" * 72)
    print(f"Case: {case_id}")
    print(
        f"Total duration: "
        f"{total_duration:.2f} seconds"
    )
    print()

    result_lookup: dict[
        str,
        dict[str, StageResult],
    ] = {}

    for result in results:
        result_lookup.setdefault(
            result.scanner,
            {},
        )[result.stage] = result

    scanner_width = max(
        10,
        max(
            len(scanner)
            for scanner in scanners
        ),
    )

    stage_width = max(
        len(stage)
        for stage in PIPELINE_STAGES
    )

    header = (
        f"{'Scanner':<{scanner_width}}  "
        f"{'Stage':<{stage_width}}  "
        f"{'Status':<8}  "
        f"{'Seconds':>8}"
    )

    print(header)
    print("-" * len(header))

    for scanner in scanners:
        scanner_results = result_lookup.get(
            scanner,
            {},
        )

        if scanner in scanner_errors:
            print(
                f"{scanner:<{scanner_width}}  "
                f"{'Preflight':<{stage_width}}  "
                f"{'FAILED':<8}  "
                f"{'—':>8}"
            )

            continue

        scanner_failed = False

        for stage_name in PIPELINE_STAGES:
            result = scanner_results.get(
                stage_name
            )

            if result is None:
                status = (
                    "SKIPPED"
                    if scanner_failed
                    else "NOT RUN"
                )

                duration_text = "—"

            else:
                status = (
                    "PASSED"
                    if result.success
                    else "FAILED"
                )

                duration_text = (
                    f"{result.duration_seconds:.2f}"
                )

                if not result.success:
                    scanner_failed = True

            print(
                f"{scanner:<{scanner_width}}  "
                f"{stage_name:<{stage_width}}  "
                f"{status:<8}  "
                f"{duration_text:>8}"
            )

    if scanner_errors:
        print()
        print("Preflight errors:")

        for scanner, message in scanner_errors.items():
            print(
                f"  [{scanner}] {message}"
            )

    failed_results = [
        result
        for result in results
        if not result.success
    ]

    if failed_results:
        print()
        print("Failed commands:")

        for result in failed_results:
            print(
                f"  [{result.scanner}] "
                f"{result.stage}"
            )

            print(
                "    "
                + format_command(
                    result.command
                )
            )

    print()
    print("=" * 72)


def run() -> int:
    """Run the complete Dockerfile benchmark pipeline."""

    arguments = parse_arguments()

    case_id = clean_text(
        arguments.case_id
    )

    if case_id is None:
        raise DockerfilePipelineError(
            "Case ID cannot be empty."
        )

    if arguments.decimal_places < 0:
        raise DockerfilePipelineError(
            "Decimal places cannot be negative."
        )

    configuration = load_benchmark_config()

    validate_dockerfile_case(
        case_id=case_id,
        configuration=configuration,
    )

    scanners = resolve_scanners(
        arguments
    )

    matching_mode = resolve_matching_mode(
        arguments=arguments,
        configuration=configuration,
    )

    validate_internal_directory(
        arguments.normalised_root,
        "Normalised root",
    )

    validate_internal_directory(
        arguments.matched_root,
        "Matched root",
    )

    validate_internal_directory(
        arguments.metrics_root,
        "Metrics root",
    )

    validate_internal_directory(
        arguments.reports_root,
        "Reports root",
    )

    validate_pipeline_scripts()

    print_pipeline_header(
        case_id=case_id,
        scanners=scanners,
        matching_mode=matching_mode,
    )

    pipeline_started_at = (
        time.perf_counter()
    )

    all_results: list[StageResult] = []
    scanner_errors: dict[str, str] = {}

    for scanner in scanners:
        print()
        print(
            f"Processing Dockerfile scanner: "
            f"{scanner}"
        )

        try:
            scanner_results = (
                run_scanner_pipeline(
                    case_id=case_id,
                    scanner=scanner,
                    matching_mode=matching_mode,
                    arguments=arguments,
                )
            )

            all_results.extend(
                scanner_results
            )

            scanner_failed = any(
                not result.success
                for result in scanner_results
            )

            if (
                scanner_failed
                and not arguments.continue_on_error
            ):
                break

        except DockerfilePipelineError as error:
            scanner_errors[scanner] = str(
                error
            )

            print()
            print(
                f"[{scanner}] Preflight: FAILED"
            )
            print(
                f"[{scanner}] {error}"
            )

            if not arguments.continue_on_error:
                break

    total_duration = (
        time.perf_counter()
        - pipeline_started_at
    )

    print_summary(
        case_id=case_id,
        scanners=scanners,
        results=all_results,
        scanner_errors=scanner_errors,
        total_duration=total_duration,
    )

    completed_scanners: set[str] = set()

    for scanner in scanners:
        scanner_results = [
            result
            for result in all_results
            if result.scanner == scanner
        ]

        if (
            len(scanner_results)
            == len(PIPELINE_STAGES)
            and all(
                result.success
                for result in scanner_results
            )
        ):
            completed_scanners.add(
                scanner
            )

    pipeline_failed = (
        bool(scanner_errors)
        or any(
            not result.success
            for result in all_results
        )
        or completed_scanners
        != set(scanners)
    )

    if pipeline_failed:
        print(
            "Dockerfile benchmark pipeline completed "
            "with one or more failures."
        )

        return 1

    print(
        "Dockerfile benchmark pipeline "
        "completed successfully."
    )

    return 0


def main() -> int:
    """Application entry point."""

    try:
        return run()

    except (
        ConfigurationError,
        DockerfilePipelineError,
    ) as error:
        print()
        print(
            "Dockerfile benchmark pipeline failed."
        )
        print(f"Reason: {error}")

        return 1

    except KeyboardInterrupt:
        print()
        print(
            "Dockerfile benchmark pipeline cancelled."
        )

        return 130

    except Exception as error:
        print()
        print(
            "Unexpected Dockerfile pipeline error."
        )
        print(
            f"{type(error).__name__}: {error}"
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())