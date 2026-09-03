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


SUPPORTED_SCANNERS = (
    "checkov",
    "trivy",
    "kubescape",
)

SUPPORTED_MATCHING_MODES = (
    "review",
    "strict",
)

PIPELINE_STAGES = (
    "Normalisation",
    "Ground-truth matching",
    "Metrics calculation",
    "Report generation",
)


class HelmPipelineError(Exception):
    """Raised when the Helm benchmark pipeline cannot run."""


@dataclass
class StageResult:
    """Result of one pipeline stage."""

    scanner: str
    stage: str
    success: bool
    return_code: int
    duration_seconds: float
    command: list[str]
    error_message: str | None = None


# This function parses command-line arguments.
def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Process existing Checkov, Trivy and Kubescape "
            "raw JSON outputs for a Helm benchmark case."
        )
    )

    parser.add_argument(
        "--case",
        required=True,
        dest="case_id",
        help="Helm benchmark case ID.",
    )

    parser.add_argument(
        "--scanners",
        nargs="+",
        default=None,
        help=(
            "Scanners to process. Supported scanners are "
            "checkov, trivy and kubescape. All three are "
            "processed when this option is omitted."
        ),
    )

    parser.add_argument(
        "--matching-mode",
        choices=SUPPORTED_MATCHING_MODES,
        default=None,
        help=(
            "Finding-matching mode. When omitted, the value "
            "from benchmark_config.yaml is used."
        ),
    )

    parser.add_argument(
        "--normalised-root",
        default="results/normalised_helm",
        help="Directory for normalised Helm findings.",
    )

    parser.add_argument(
        "--matched-root",
        default="results/matched_helm",
        help="Directory for matched Helm findings.",
    )

    parser.add_argument(
        "--metrics-root",
        default="results/metrics_helm",
        help="Directory for Helm metrics.",
    )

    parser.add_argument(
        "--reports-root",
        default="results/reports_helm",
        help="Directory for Helm Markdown reports.",
    )

    parser.add_argument(
        "--decimal-places",
        type=int,
        default=4,
        help="Number of decimal places used for calculated metrics.",
    )

    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help=(
            "Continue processing other scanners when one "
            "scanner or stage fails."
        ),
    )

    return parser.parse_args()


# This function returns a stripped string or None.
def clean_text(value: Any) -> str | None:
    """Return a stripped string or None."""

    if not isinstance(value, str):
        return None

    cleaned = value.strip()

    return cleaned or None


# This function removes duplicates while preserving their original order.
def remove_duplicates(values: list[str]) -> list[str]:
    """Remove duplicates while preserving their original order."""

    unique_values: list[str] = []
    seen_values: set[str] = set()

    for value in values:
        if value in seen_values:
            continue

        seen_values.add(value)
        unique_values.append(value)

    return unique_values


# This function resolves and validates the selected scanners.
def resolve_scanners(arguments: argparse.Namespace) -> list[str]:
    """Resolve and validate the selected scanners."""

    # A scanner list entered on the command line overrides the built-in defaults.
    requested_scanners = (
        arguments.scanners
        if arguments.scanners
        else list(SUPPORTED_SCANNERS)
    )

    scanners: list[str] = []

    for value in requested_scanners:
        scanner = clean_text(value)

        if scanner is None:
            raise HelmPipelineError(
                f"Invalid scanner value: {value!r}"
            )

        scanner = scanner.lower()

        if scanner not in SUPPORTED_SCANNERS:
            supported = ", ".join(SUPPORTED_SCANNERS)

            raise HelmPipelineError(
                f"Scanner '{scanner}' is not supported by the "
                f"Helm runner. Supported scanners: {supported}."
            )

        scanners.append(scanner)

    scanners = remove_duplicates(scanners)

    if not scanners:
        raise HelmPipelineError(
            "No Helm scanners were selected."
        )

    return scanners


# This function resolves matching mode from arguments or configuration.
def resolve_matching_mode(
    arguments: argparse.Namespace,
    configuration: dict[str, Any],
) -> str:
    """Resolve matching mode from arguments or configuration."""

    # A command-line mode overrides the configured mode and its review fallback.
    if arguments.matching_mode:
        matching_mode = arguments.matching_mode

    else:
        defaults = configuration.get("defaults", {})

        if not isinstance(defaults, dict):
            defaults = {}

        matching_mode = defaults.get(
            "matching_mode",
            "review",
        )

    matching_mode = str(matching_mode).strip().lower()

    if matching_mode not in SUPPORTED_MATCHING_MODES:
        raise HelmPipelineError(
            "Matching mode must be 'review' or 'strict'."
        )

    return matching_mode


# This function resolves a project-relative path and ensures that it remains inside the benchmark project.
def resolve_project_path(
    path_value: Any,
    field_name: str,
) -> Path:
    """
    Resolve a project-relative path and ensure that it remains
    inside the benchmark project.
    """

    clean_path = clean_text(path_value)

    if clean_path is None:
        raise HelmPipelineError(
            f"{field_name} must be a non-empty string."
        )

    resolved_path = (
        PROJECT_ROOT
        / clean_path
    ).resolve()

    # Reject path traversal so configured files cannot escape the project directory.
    try:
        resolved_path.relative_to(
            PROJECT_ROOT.resolve()
        )

    except ValueError as error:
        raise HelmPipelineError(
            f"{field_name} must remain inside the project directory."
        ) from error

    return resolved_path


# This function validates an output directory path.
def validate_output_directory(
    directory_value: str,
    field_name: str,
) -> Path:
    """Validate an output directory path."""

    return resolve_project_path(
        path_value=directory_value,
        field_name=field_name,
    )


# This function confirms that the requested case is a valid Helm case.
def validate_helm_case(
    case_id: str,
    configuration: dict[str, Any],
) -> dict[str, Any]:
    """Confirm that the requested case is a valid Helm case."""

    case_configuration = get_case_configuration(
        configuration,
        case_id,
    )

    artifact_type = clean_text(
        case_configuration.get("artifact_type")
    )

    if artifact_type is None:
        raise HelmPipelineError(
            f"Case '{case_id}' does not contain a valid artifact_type."
        )

    artifact_type = artifact_type.lower()

    if artifact_type != "helm_chart":
        raise HelmPipelineError(
            f"Case '{case_id}' has artifact type '{artifact_type}'. "
            "The Helm runner only accepts artifact_type: helm_chart."
        )

    chart_path = resolve_project_path(
        case_configuration.get("artifact_path"),
        f"cases.{case_id}.artifact_path",
    )

    if not chart_path.exists():
        raise HelmPipelineError(
            "Helm chart directory does not exist: "
            f"{chart_path.relative_to(PROJECT_ROOT)}"
        )

    if not chart_path.is_dir():
        raise HelmPipelineError(
            "Helm artifact path must be a directory: "
            f"{chart_path.relative_to(PROJECT_ROOT)}"
        )

    chart_yaml = chart_path / "Chart.yaml"

    if not chart_yaml.is_file():
        raise HelmPipelineError(
            "Helm chart is missing Chart.yaml: "
            f"{chart_yaml.relative_to(PROJECT_ROOT)}"
        )

    templates_directory = chart_path / "templates"

    if not templates_directory.is_dir():
        raise HelmPipelineError(
            "Helm chart is missing its templates directory: "
            f"{templates_directory.relative_to(PROJECT_ROOT)}"
        )

    template_files = [
        path
        for path in templates_directory.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {
            ".yaml",
            ".yml",
            ".tpl",
        }
    ]

    if not template_files:
        raise HelmPipelineError(
            "The Helm chart templates directory contains no "
            "YAML or template files."
        )

    ground_truth_path = resolve_project_path(
        case_configuration.get("ground_truth_path"),
        f"cases.{case_id}.ground_truth_path",
    )

    if not ground_truth_path.exists():
        raise HelmPipelineError(
            "Ground-truth file does not exist: "
            f"{ground_truth_path.relative_to(PROJECT_ROOT)}"
        )

    if not ground_truth_path.is_file():
        raise HelmPipelineError(
            "Ground-truth path is not a file: "
            f"{ground_truth_path.relative_to(PROJECT_ROOT)}"
        )

    rule_mappings = case_configuration.get(
        "rule_mappings"
    )

    if not isinstance(rule_mappings, dict):
        raise HelmPipelineError(
            f"Case '{case_id}' does not contain valid rule_mappings."
        )

    return case_configuration


# This function confirms that the shared analysis scripts exist.
def validate_shared_scripts() -> None:
    """Confirm that the shared analysis scripts exist."""

    required_scripts = (
        "normalize_findings.py",
        "match_findings.py",
        "compute_metrics.py",
        "generate_report.py",
    )

    missing_scripts: list[str] = []

    for script_name in required_scripts:
        script_path = (
            PROJECT_ROOT
            / "scripts"
            / script_name
        )

        if not script_path.is_file():
            missing_scripts.append(
                str(
                    script_path.relative_to(
                        PROJECT_ROOT
                    )
                )
            )

    if missing_scripts:
        formatted_paths = "\n".join(
            f"  - {path}"
            for path in missing_scripts
        )

        raise HelmPipelineError(
            "The following shared pipeline scripts are missing:\n"
            f"{formatted_paths}"
        )


# This function returns the expected scanner raw-output path.
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


# This function confirms that a raw scanner JSON file exists.
def validate_raw_output(
    scanner: str,
    case_id: str,
) -> Path:
    """Confirm that a raw scanner JSON file exists."""

    output_path = raw_output_path(
        scanner,
        case_id,
    )

    if not output_path.exists():
        raise HelmPipelineError(
            f"Raw {scanner} output does not exist: "
            f"{output_path.relative_to(PROJECT_ROOT)}"
        )

    if not output_path.is_file():
        raise HelmPipelineError(
            f"Raw {scanner} output path is not a file: "
            f"{output_path.relative_to(PROJECT_ROOT)}"
        )

    if output_path.stat().st_size == 0:
        raise HelmPipelineError(
            f"Raw {scanner} output is empty: "
            f"{output_path.relative_to(PROJECT_ROOT)}"
        )

    return output_path


# This function creates a readable command string.
def format_command(command: list[str]) -> str:
    """Create a readable command string."""

    if os.name == "nt":
        return subprocess.list2cmdline(command)

    return shlex.join(command)


# This function prints the pipeline configuration.
def print_pipeline_header(
    case_id: str,
    scanners: list[str],
    matching_mode: str,
) -> None:
    """Print the pipeline configuration."""

    separator = "=" * 76

    print()
    print(separator)
    print("Helm benchmark pipeline")
    print(f"Case: {case_id}")
    print(f"Matching mode: {matching_mode}")
    print(f"Scanners: {', '.join(scanners)}")
    print(separator)


# This function prints information before a stage starts.
def print_stage_header(
    scanner: str,
    stage: str,
    command: list[str],
) -> None:
    """Print information before a stage starts."""

    print()
    print("-" * 76)
    print(f"[{scanner}] Starting stage: {stage}")
    print(
        f"[{scanner}] Command: "
        f"{format_command(command)}"
    )
    print("-" * 76)


# This function runs one pipeline stage and streams its output.
def run_stage(
    scanner: str,
    stage: str,
    command: list[str],
) -> StageResult:
    """Run one pipeline stage and stream its output."""

    print_stage_header(
        scanner=scanner,
        stage=stage,
        command=command,
    )

    started_at = time.perf_counter()

    environment = os.environ.copy()
    # Unbuffered output lets the parent display child-script output immediately.
    environment["PYTHONUNBUFFERED"] = "1"

    try:
        process = subprocess.Popen(
            command,
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            # Combining both streams preserves the order of output and errors.
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            env=environment,
        )

    except OSError as error:
        duration = time.perf_counter() - started_at

        message = f"Could not start stage: {error}"

        print(f"[{scanner}] {stage}: FAILED")
        print(f"[{scanner}] {message}")

        return StageResult(
            scanner=scanner,
            stage=stage,
            success=False,
            return_code=1,
            duration_seconds=duration,
            command=command,
            error_message=message,
        )

    if process.stdout is not None:
        for line in process.stdout:
            print(line, end="")

    return_code = process.wait()
    duration = time.perf_counter() - started_at
    success = return_code == 0

    status = "PASSED" if success else "FAILED"

    print()
    print(
        f"[{scanner}] {stage}: {status} "
        f"({duration:.2f} seconds)"
    )

    error_message = None

    if not success:
        error_message = (
            f"Stage returned exit code {return_code}."
        )

        print(f"[{scanner}] {error_message}")

    return StageResult(
        scanner=scanner,
        stage=stage,
        success=success,
        return_code=return_code,
        duration_seconds=duration,
        command=command,
        error_message=error_message,
    )


# This function builds the shared analysis commands for one scanner.
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
    """Build the shared analysis commands for one scanner."""

    scripts_directory = (
        PROJECT_ROOT
        / "scripts"
    )

    # Use the same Python interpreter and virtual environment as this runner.
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

    # The stages must stay ordered because each one reads the previous stage's output.
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


# This function runs all analysis stages for one scanner.
def run_scanner_pipeline(
    case_id: str,
    scanner: str,
    matching_mode: str,
    arguments: argparse.Namespace,
) -> list[StageResult]:
    """Run all analysis stages for one scanner."""

    # The runner processes saved JSON and intentionally does not execute scanner CLIs.
    validate_raw_output(
        scanner=scanner,
        case_id=case_id,
    )

    commands = build_pipeline_commands(
        case_id=case_id,
        scanner=scanner,
        matching_mode=matching_mode,
        normalised_root=arguments.normalised_root,
        matched_root=arguments.matched_root,
        metrics_root=arguments.metrics_root,
        reports_root=arguments.reports_root,
        decimal_places=arguments.decimal_places,
    )

    results: list[StageResult] = []

    for stage, command in commands:
        result = run_stage(
            scanner=scanner,
            stage=stage,
            command=command,
        )

        results.append(result)

        # Later stages depend on this output, so they cannot run after a failure.
        if not result.success:
            break

    return results


# This function prints the final pipeline summary.
def print_summary(
    case_id: str,
    scanners: list[str],
    results: list[StageResult],
    scanner_errors: dict[str, str],
    total_duration: float,
) -> None:
    """Print the final pipeline summary."""

    print()
    print("=" * 76)
    print("Helm benchmark pipeline summary")
    print("=" * 76)
    print(f"Case: {case_id}")
    print(f"Total duration: {total_duration:.2f} seconds")
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
        max(len(scanner) for scanner in scanners),
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
        if scanner in scanner_errors:
            print(
                f"{scanner:<{scanner_width}}  "
                f"{'Preflight':<{stage_width}}  "
                f"{'FAILED':<8}  "
                f"{'—':>8}"
            )

            continue

        scanner_results = result_lookup.get(
            scanner,
            {},
        )

        previous_stage_failed = False

        for stage_name in PIPELINE_STAGES:
            stage_result = scanner_results.get(
                stage_name
            )

            if stage_result is None:
                status = (
                    "SKIPPED"
                    if previous_stage_failed
                    else "NOT RUN"
                )

                duration_text = "—"

            else:
                status = (
                    "PASSED"
                    if stage_result.success
                    else "FAILED"
                )

                duration_text = (
                    f"{stage_result.duration_seconds:.2f}"
                )

                if not stage_result.success:
                    previous_stage_failed = True

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
            print(f"  [{scanner}] {message}")

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
    print("=" * 76)


# This function runs the complete Helm benchmark analysis pipeline.
def run() -> int:
    """Run the complete Helm benchmark analysis pipeline."""

    arguments = parse_arguments()

    case_id = clean_text(
        arguments.case_id
    )

    if case_id is None:
        raise HelmPipelineError(
            "Case ID cannot be empty."
        )

    if arguments.decimal_places < 0:
        raise HelmPipelineError(
            "Decimal places cannot be negative."
        )

    configuration = load_benchmark_config()

    validate_helm_case(
        case_id=case_id,
        configuration=configuration,
    )

    scanners = resolve_scanners(arguments)

    matching_mode = resolve_matching_mode(
        arguments=arguments,
        configuration=configuration,
    )

    validate_output_directory(
        arguments.normalised_root,
        "Normalised output root",
    )

    validate_output_directory(
        arguments.matched_root,
        "Matched output root",
    )

    validate_output_directory(
        arguments.metrics_root,
        "Metrics output root",
    )

    validate_output_directory(
        arguments.reports_root,
        "Reports output root",
    )

    validate_shared_scripts()

    print_pipeline_header(
        case_id=case_id,
        scanners=scanners,
        matching_mode=matching_mode,
    )

    pipeline_started_at = time.perf_counter()

    all_results: list[StageResult] = []
    scanner_errors: dict[str, str] = {}

    for scanner in scanners:
        print()
        print(
            f"Processing Helm scanner: {scanner}"
        )

        try:
            scanner_results = run_scanner_pipeline(
                case_id=case_id,
                scanner=scanner,
                matching_mode=matching_mode,
                arguments=arguments,
            )

            all_results.extend(
                scanner_results
            )

            scanner_failed = any(
                not result.success
                for result in scanner_results
            )

            # This flag decides whether a failed scanner also stops later scanners.
            if (
                scanner_failed
                and not arguments.continue_on_error
            ):
                break

        except HelmPipelineError as error:
            scanner_errors[scanner] = str(error)

            print()
            print(f"[{scanner}] Preflight: FAILED")
            print(f"[{scanner}] {error}")

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
            completed_scanners.add(scanner)

    pipeline_failed = (
        bool(scanner_errors)
        or any(
            not result.success
            for result in all_results
        )
        or completed_scanners != set(scanners)
    )

    if pipeline_failed:
        print(
            "Helm benchmark pipeline completed "
            "with one or more failures."
        )

        return 1

    print(
        "Helm benchmark pipeline completed successfully."
    )

    return 0


# This function serves as the application entry point and handles any errors.
def main() -> int:
    """Application entry point."""

    try:
        return run()

    except (
        ConfigurationError,
        HelmPipelineError,
    ) as error:
        print()
        print("Helm benchmark pipeline failed.")
        print(f"Reason: {error}")

        return 1

    except KeyboardInterrupt:
        print()
        print("Helm benchmark pipeline cancelled.")

        return 130

    except Exception as error:
        print()
        print("Unexpected Helm pipeline error.")
        print(
            f"{type(error).__name__}: {error}"
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())
