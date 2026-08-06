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

# scanners
SUPPORTED_SCANNERS = {
    "checkov",
    "trivy",
    "kubescape",
}

# modes
SUPPORTED_MATCHING_MODES = {
    "review",
    "strict",
}

# exception handling
class PipelineError(Exception):
    """Raised when the benchmark pipeline cannot run."""


@dataclass
class StageResult:
    """Stores the result of one pipeline stage."""
# results stored
    scanner: str
    stage: str
    success: bool
    return_code: int
    duration_seconds: float
    command: list[str]
    error_message: str | None = None

# This function reads command-line arguments.
def parse_arguments() -> argparse.Namespace:
    """Read command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Run the generic scanner benchmark pipeline "
            "from existing raw scanner JSON outputs."
        )
    )

    parser.add_argument(
        "--case",
        required=True,
        dest="case_id",
        help="Benchmark case ID.",
    )

    parser.add_argument(
        "--scanners",
        nargs="+",
        default=None,
        help=(
            "Scanners to process. Supported values are "
            "checkov, trivy and kubescape. When omitted, "
            "the scanner list from benchmark_config.yaml "
            "is used."
        ),
    )

    parser.add_argument(
        "--matching-mode",
        choices=sorted(SUPPORTED_MATCHING_MODES),
        default=None,
        help=(
            "Matching mode. When omitted, the default "
            "from benchmark_config.yaml is used."
        ),
    )

    parser.add_argument(
        "--normalised-root",
        default="results/normalised_generic",
        help="Directory for generic normalised findings.",
    )

    parser.add_argument(
        "--matched-root",
        default="results/matched_generic",
        help="Directory for generic matched findings.",
    )

    parser.add_argument(
        "--metrics-root",
        default="results/metrics_generic",
        help="Directory for generic metrics.",
    )

    parser.add_argument(
        "--reports-root",
        default="results/reports_generic",
        help="Directory for generic Markdown reports.",
    )

    parser.add_argument(
        "--decimal-places",
        type=int,
        default=4,
        help=(
            "Number of decimal places used by "
            "compute_metrics.py."
        ),
    )

    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help=(
            "Continue with the remaining scanners when "
            "one scanner fails. By default, the pipeline "
            "stops after the first failure."
        ),
    )

    return parser.parse_args()

# This function cleans and validates one scanner name.
def clean_scanner_name(value: Any) -> str:
    """Clean and validate one scanner name."""

    if not isinstance(value, str):
        raise PipelineError(
            f"Invalid scanner value: {value!r}"
        )

    scanner = value.strip().lower()

    if scanner not in SUPPORTED_SCANNERS:
        supported = ", ".join(
            sorted(SUPPORTED_SCANNERS)
        )

        raise PipelineError(
            f"Unsupported scanner '{scanner}'. "
            f"Supported scanners: {supported}."
        )

    return scanner

# This function removes duplicates while preserving order.
def remove_duplicates(
    values: list[str],
) -> list[str]:
    """Remove duplicates while preserving order."""

    unique_values: list[str] = []
    seen: set[str] = set()

    for value in values:
        if value in seen:
            continue

        seen.add(value)
        unique_values.append(value)

    return unique_values

# This function resolves scanners from CLI arguments or configuration.
def resolve_scanners(
    arguments: argparse.Namespace,
    configuration: dict[str, Any],
) -> list[str]:
    """Resolve scanners from CLI arguments or configuration."""

    # A scanner list entered on the command line overrides the configured defaults.
    if arguments.scanners:
        scanner_values = arguments.scanners
    else:
        defaults = configuration.get(
            "defaults",
            {},
        )

        if not isinstance(defaults, dict):
            defaults = {}

        configured_scanners = defaults.get(
            "scanners",
            [],
        )

        if not isinstance(
            configured_scanners,
            list,
        ):
            raise PipelineError(
                "defaults.scanners in "
                "benchmark_config.yaml must be a list."
            )

        scanner_values = configured_scanners

    scanners = [
        clean_scanner_name(value)
        for value in scanner_values
    ]

    scanners = remove_duplicates(
        scanners
    )

    if not scanners:
        raise PipelineError(
            "No scanners were selected."
        )

    return scanners

# This function resolves matching mode from CLI or configuration.
def resolve_matching_mode(
    arguments: argparse.Namespace,
    configuration: dict[str, Any],
) -> str:
    """Resolve matching mode from CLI or configuration."""

    # A command-line mode overrides the configured mode and its review fallback.
    if arguments.matching_mode:
        mode = arguments.matching_mode
    else:
        defaults = configuration.get(
            "defaults",
            {},
        )

        if not isinstance(defaults, dict):
            defaults = {}

        mode = defaults.get(
            "matching_mode",
            "review",
        )

    mode = str(mode).strip().lower()

    if mode not in SUPPORTED_MATCHING_MODES:
        raise PipelineError(
            "Matching mode must be 'review' "
            "or 'strict'."
        )

    return mode

# This function confirms that an output directory remains inside the benchmark project.
def validate_internal_directory(
    directory_value: str,
    field_name: str,
) -> Path:
    """
    Confirm that an output directory remains inside
    the benchmark project.
    """

    directory = (
        PROJECT_ROOT / directory_value
    ).resolve()

    # Reject path traversal so pipeline output cannot escape the project directory.
    try:
        directory.relative_to(PROJECT_ROOT)

    except ValueError as error:
        raise PipelineError(
            f"{field_name} must be inside "
            "the project directory."
        ) from error

    return directory

# This function confirms that every pipeline script exists.
def validate_script_files() -> None:
    """Confirm that every pipeline script exists."""

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
        formatted_paths = "\n".join(
            f"  - {path}"
            for path in missing_scripts
        )

        raise PipelineError(
            "The following pipeline scripts "
            f"are missing:\n{formatted_paths}"
        )

# This function returns the expected raw scanner JSON path.
def raw_output_path(
    scanner: str,
    case_id: str,
) -> Path:
    """Return the expected raw scanner JSON path."""

    return (
        PROJECT_ROOT
        / "results"
        / "raw"
        / scanner
        / f"{case_id}.json"
    )

# This function confirms that a scanner raw-output file exists.
def validate_raw_output(
    scanner: str,
    case_id: str,
) -> Path:
    """Confirm that a scanner raw-output file exists."""

    path = raw_output_path(
        scanner,
        case_id,
    )

    if not path.exists():
        raise PipelineError(
            f"Raw {scanner} output does not exist: "
            f"{path.relative_to(PROJECT_ROOT)}"
        )

    if not path.is_file():
        raise PipelineError(
            f"Raw {scanner} output is not a file: "
            f"{path.relative_to(PROJECT_ROOT)}"
        )

    return path

# This function creates a readable representation of a command.
def format_command(
    command: list[str],
) -> str:
    """Create a readable representation of a command."""

    if os.name == "nt":
        return subprocess.list2cmdline(
            command
        )

    return shlex.join(command)

# This function displays the pipeline configuration.
def print_pipeline_header(
    case_id: str,
    scanners: list[str],
    matching_mode: str,
) -> None:
    """Display the pipeline configuration."""

    separator = "=" * 72

    print()
    print(separator)
    print(f"Benchmark case: {case_id}")
    print(f"Matching mode: {matching_mode}")
    print(
        "Scanners: "
        + ", ".join(scanners)
    )
    print(separator)
    print()

# This function displays information before a stage starts.
def print_stage_header(
    scanner: str,
    stage: str,
    command: list[str],
) -> None:
    """Display information before a stage starts."""

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

# This function runs one Python pipeline stage and streams its console output.
def run_stage(
    scanner: str,
    stage: str,
    command: list[str],
) -> StageResult:
    """
    Run one Python pipeline stage and stream its
    console output.
    """

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
        duration = (
            time.perf_counter()
            - started_at
        )

        message = (
            f"Could not start the stage: {error}"
        )

        print(
            f"[{scanner}] {stage}: FAILED"
        )
        print(
            f"[{scanner}] {message}"
        )

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

# This function builds the ordered commands for one scanner.
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
    """Build the ordered commands for one scanner."""

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

# This function runs every pipeline stage for one scanner.
def run_scanner_pipeline(
    case_id: str,
    scanner: str,
    matching_mode: str,
    arguments: argparse.Namespace,
) -> list[StageResult]:
    """Run every pipeline stage for one scanner."""

    results: list[StageResult] = []

    # The runner processes saved JSON and intentionally does not execute scanner CLIs.
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

# This function displays the final pipeline summary.
def print_summary(
    case_id: str,
    scanners: list[str],
    results: list[StageResult],
    scanner_errors: dict[str, str],
    total_duration: float,
) -> None:
    """Display the final pipeline summary."""

    print()
    print("=" * 72)
    print("Benchmark pipeline summary")
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

    stage_names = [
        "Normalisation",
        "Ground-truth matching",
        "Metrics calculation",
        "Report generation",
    ]

    scanner_width = max(
        10,
        max(
            len(scanner)
            for scanner in scanners
        ),
    )

    stage_width = max(
        len(stage)
        for stage in stage_names
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

        scanner_error = scanner_errors.get(
            scanner
        )

        if scanner_error is not None:
            print(
                f"{scanner:<{scanner_width}}  "
                f"{'Preflight':<{stage_width}}  "
                f"{'FAILED':<8}  "
                f"{'—':>8}"
            )

            continue

        scanner_failed = False

        for stage_name in stage_names:
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

        for scanner, message in (
            scanner_errors.items()
        ):
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

# This function runs the complete benchmark pipeline.
def run() -> int:
    """Run the complete benchmark pipeline."""

    arguments = parse_arguments()

    case_id = arguments.case_id.strip()

    if not case_id:
        raise PipelineError(
            "Case ID cannot be empty."
        )

    if arguments.decimal_places < 0:
        raise PipelineError(
            "Decimal places cannot be negative."
        )

    configuration = load_benchmark_config()

    # Confirms that the case exists in
    # benchmark_config.yaml.
    get_case_configuration(
        configuration,
        case_id,
    )

    scanners = resolve_scanners(
        arguments=arguments,
        configuration=configuration,
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

    validate_script_files()

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

    stop_pipeline = False

    for scanner in scanners:
        if stop_pipeline:
            break

        print()
        print(
            f"Processing scanner: {scanner}"
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

            # This flag decides whether a failed scanner also stops later scanners.
            if (
                scanner_failed
                and not arguments.continue_on_error
            ):
                stop_pipeline = True

        except PipelineError as error:
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
                stop_pipeline = True

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

    pipeline_failed = (
        bool(scanner_errors)
        or any(
            not result.success
            for result in all_results
        )
        or len(
            {
                result.scanner
                for result in all_results
            }
        )
        < (
            len(scanners)
            - len(scanner_errors)
        )
    )

    if pipeline_failed:
        print(
            "Benchmark pipeline completed "
            "with one or more failures."
        )
        # Exit code 1 tells a terminal or CI system that the benchmark failed.
        return 1

    print(
        "Benchmark pipeline completed successfully."
    )

    # Exit code 0 tells a terminal or CI system that the benchmark succeeded.
    return 0

# This function serves as the application entry point and handles any errors.
def main() -> int:
    """Application entry point."""

    try:
        return run()

    except (
        ConfigurationError,
        PipelineError,
    ) as error:
        print()
        print("Benchmark pipeline failed.")
        print(f"Reason: {error}")
        return 1

    except KeyboardInterrupt:
        print()
        print("Benchmark pipeline cancelled.")
        # Exit code 130 is the conventional result for a keyboard interruption.
        return 130

    except Exception as error:
        print()
        print("Unexpected benchmark pipeline error.")
        print(
            f"{type(error).__name__}: {error}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
