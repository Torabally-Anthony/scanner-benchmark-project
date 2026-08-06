from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from config_loader import (
    PROJECT_ROOT,
    ConfigurationError,
    build_rule_to_ground_truth_map,
    get_case_configuration,
    get_ground_truth_items,
    load_benchmark_config,
    load_case_ground_truth,
)


SUPPORTED_SCANNERS = {
    "checkov",
    "trivy",
    "kubescape",
}


class NormalisationError(Exception):
    """Raised when scanner output cannot be normalised."""


# This function reads a JSON file, including files containing a UTF-8 BOM.
def read_json(path: Path) -> Any:
    """Read a JSON file, including files containing a UTF-8 BOM."""

    if not path.exists():
        raise NormalisationError(
            f"Raw scanner output does not exist: {path}"
        )

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        raise NormalisationError(
            f"Invalid JSON in {path.name}: {error}"
        ) from error

    except OSError as error:
        raise NormalisationError(
            f"Could not read {path}: {error}"
        ) from error


# This function reads the scanner version saved in the raw results directory.
def read_scanner_version(scanner: str) -> str:
    """Read the scanner version saved in the raw results directory."""

    version_path = (
        PROJECT_ROOT
        / "results"
        / "raw"
        / scanner
        / f"{scanner}-version.txt"
    )

    if not version_path.exists():
        return "Unknown"

    try:
        return version_path.read_text(
            encoding="utf-8-sig"
        ).strip()

    except OSError:
        return "Unknown"


# This function converts a scanner line range into start and end values.
def parse_line_range(
    value: Any,
) -> tuple[int | None, int | None]:
    """Convert a scanner line range into start and end values."""

    if isinstance(value, list) and len(value) >= 2:
        start_line = value[0]
        end_line = value[1]

        return (
            start_line if isinstance(start_line, int) else None,
            end_line if isinstance(end_line, int) else None,
        )

    return None, None


# This function extracts failed findings from Checkov JSON.
def extract_checkov_findings(
    raw_data: Any,
) -> list[dict[str, Any]]:
    """Extract failed findings from Checkov JSON."""

    blocks: list[dict[str, Any]]

    if isinstance(raw_data, dict):
        blocks = [raw_data]

    elif isinstance(raw_data, list):
        blocks = [
            item
            for item in raw_data
            if isinstance(item, dict)
        ]

    else:
        raise NormalisationError(
            "Unexpected Checkov JSON structure."
        )

    extracted: list[dict[str, Any]] = []

    for block in blocks:
        results = block.get("results", {})

        if not isinstance(results, dict):
            continue

        failed_checks = results.get(
            "failed_checks",
            [],
        )

        if not isinstance(failed_checks, list):
            continue

        for finding in failed_checks:
            if not isinstance(finding, dict):
                continue

            start_line, end_line = parse_line_range(
                finding.get("file_line_range")
            )

            check_result = finding.get(
                "check_result",
                {},
            )

            if isinstance(check_result, dict):
                status = (
                    check_result.get("result")
                    or "FAILED"
                )
            else:
                status = "FAILED"

            extracted.append(
                {
                    "rule_id": finding.get("check_id"),
                    "rule_name": finding.get("check_name"),
                    "severity": finding.get("severity"),
                    "status": status,
                    "message": finding.get("check_name"),
                    "resource": finding.get("resource"),
                    "container": None,
                    "field_path": None,
                    "original_category": finding.get(
                        "bc_category"
                    ),
                    "original_subcategory": None,
                    "source_file": (
                        finding.get("repo_file_path")
                        or finding.get("file_path")
                    ),
                    "line_start": start_line,
                    "line_end": end_line,
                    "failed_resources": None,
                    "passed_resources": None,
                    "skipped_resources": None,
                    "score": None,
                    "compliance_score": None,
                }
            )

    return extracted


# This function extracts failed misconfigurations from Trivy JSON.
def extract_trivy_findings(
    raw_data: Any,
) -> list[dict[str, Any]]:
    """Extract failed misconfigurations from Trivy JSON."""

    if not isinstance(raw_data, dict):
        raise NormalisationError(
            "Unexpected Trivy JSON structure."
        )

    results = raw_data.get("Results", [])

    if not isinstance(results, list):
        raise NormalisationError(
            "Trivy JSON has no valid Results list."
        )

    extracted: list[dict[str, Any]] = []

    for result in results:
        if not isinstance(result, dict):
            continue

        target = result.get("Target")

        misconfigurations = result.get(
            "Misconfigurations",
            [],
        )

        if not isinstance(misconfigurations, list):
            continue

        for finding in misconfigurations:
            if not isinstance(finding, dict):
                continue

            cause_metadata = finding.get(
                "CauseMetadata",
                {},
            )

            if not isinstance(cause_metadata, dict):
                cause_metadata = {}

            extracted.append(
                {
                    "rule_id": (
                        finding.get("ID")
                        or finding.get("AVDID")
                    ),
                    "rule_name": finding.get("Title"),
                    "severity": finding.get("Severity"),
                    "status": (
                        finding.get("Status")
                        or "FAIL"
                    ),
                    "message": (
                        finding.get("Message")
                        or finding.get("Description")
                    ),
                    "resource": target,
                    "container": None,
                    "field_path": None,
                    "original_category": result.get("Class"),
                    "original_subcategory": result.get("Type"),
                    "source_file": target,
                    "line_start": cause_metadata.get(
                        "StartLine"
                    ),
                    "line_end": cause_metadata.get(
                        "EndLine"
                    ),
                    "failed_resources": None,
                    "passed_resources": None,
                    "skipped_resources": None,
                    "score": None,
                    "compliance_score": None,
                }
            )

    return extracted


# This function extracts failed controls from Kubescape JSON.
def extract_kubescape_findings(
    raw_data: Any,
) -> list[dict[str, Any]]:
    """Extract failed controls from Kubescape JSON."""

    if not isinstance(raw_data, dict):
        raise NormalisationError(
            "Unexpected Kubescape JSON structure."
        )

    summary_details = raw_data.get(
        "summaryDetails",
        {},
    )

    if not isinstance(summary_details, dict):
        raise NormalisationError(
            "Kubescape JSON has no valid "
            "summaryDetails object."
        )

    controls_data = summary_details.get(
        "controls",
        {},
    )

    # Kubescape normally stores its controls as a dictionary:
    #
    # "controls": {
    #     "C-0004": {...},
    #     "C-0057": {...}
    # }
    #
    # Some versions may use a list, so both forms are supported.
    if isinstance(controls_data, dict):
        controls = list(controls_data.values())

    elif isinstance(controls_data, list):
        controls = controls_data

    else:
        raise NormalisationError(
            "Kubescape summaryDetails.controls must "
            "be an object or list."
        )

    extracted: list[dict[str, Any]] = []

    for control in controls:
        if not isinstance(control, dict):
            continue

        status_info = control.get(
            "statusInfo",
            {},
        )

        if not isinstance(status_info, dict):
            status_info = {}

        status = str(
            control.get("status")
            or status_info.get("status")
            or ""
        ).strip().lower()

        resource_counters = control.get(
            "ResourceCounters",
            {},
        )

        if not isinstance(resource_counters, dict):
            resource_counters = {}

        failed_resources = resource_counters.get(
            "failedResources",
            0,
        )

        passed_resources = resource_counters.get(
            "passedResources",
            0,
        )

        skipped_resources = resource_counters.get(
            "skippedResources",
            0,
        )

        is_failed = (
            status in {"failed", "fail"}
            or (
                isinstance(failed_resources, int)
                and failed_resources > 0
            )
        )

        if not is_failed:
            continue

        category_data = control.get(
            "category",
            {},
        )

        if not isinstance(category_data, dict):
            category_data = {}

        subcategory_data = category_data.get(
            "subCategory",
            {},
        )

        if not isinstance(subcategory_data, dict):
            subcategory_data = {}

        rule_id = (
            control.get("controlID")
            or control.get("id")
        )

        rule_name = control.get("name")

        message = (
            f"Kubescape control {rule_id} failed: "
            f"{rule_name}"
        )

        extracted.append(
            {
                "rule_id": rule_id,
                "rule_name": rule_name,
                "severity": control.get("severity"),
                "status": status.upper() or "FAILED",
                "message": message,
                "resource": "Unknown",
                "container": None,
                "field_path": None,
                "original_category": (
                    category_data.get("name")
                ),
                "original_subcategory": (
                    subcategory_data.get("name")
                ),
                "source_file": None,
                "line_start": None,
                "line_end": None,
                "failed_resources": failed_resources,
                "passed_resources": passed_resources,
                "skipped_resources": skipped_resources,
                "score": control.get("score"),
                "compliance_score": control.get(
                    "complianceScore"
                ),
            }
        )

    return extracted


# This function sends raw scanner data to the correct scanner extractor.
def extract_scanner_findings(
    scanner: str,
    raw_data: Any,
) -> list[dict[str, Any]]:
    """Send raw scanner data to the correct scanner extractor."""

    extractors: dict[
        str,
        Callable[[Any], list[dict[str, Any]]],
    ] = {
        "checkov": extract_checkov_findings,
        "trivy": extract_trivy_findings,
        "kubescape": extract_kubescape_findings,
    }

    # Scanner-specific parsing ends here; every later stage receives one common schema.
    extractor = extractors.get(scanner)

    if extractor is None:
        raise NormalisationError(
            f"Unsupported scanner: {scanner}"
        )

    return extractor(raw_data)


# This function creates the common resource name from ground truth.
def canonical_resource(
    ground_truth_item: dict[str, Any],
) -> tuple[str | None, str | None]:
    """Create the common resource name from ground truth."""

    resource = ground_truth_item.get("resource")

    if isinstance(resource, str):
        return (
            resource,
            ground_truth_item.get("container"),
        )

    if not isinstance(resource, dict):
        return (
            None,
            ground_truth_item.get("container"),
        )

    kind = resource.get("kind")
    namespace = resource.get(
        "namespace",
        "default",
    )
    name = resource.get("name")

    resource_parts = [
        str(value)
        for value in (
            kind,
            namespace,
            name,
        )
        if value is not None
    ]

    resource_name = (
        ".".join(resource_parts)
        if resource_parts
        else None
    )

    container = (
        resource.get("container")
        or ground_truth_item.get("container")
    )

    return resource_name, container


# This function cleans scanner rule IDs before matching.
def normalise_rule_id(
    rule_id: Any,
) -> str | None:
    """Clean scanner rule IDs before matching."""

    if not isinstance(rule_id, str):
        return None

    clean_rule_id = rule_id.strip().upper()

    return clean_rule_id or None


# This function converts extracted findings into the common schema.
def normalise_findings(
    scanner: str,
    case_id: str,
    artifact_type: str,
    extracted_findings: list[dict[str, Any]],
    reverse_rule_mapping: dict[str, str],
    ground_truth_items: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Convert extracted findings into the common schema."""

    cleaned_rule_mapping = {
        clean_rule_id: ground_truth_id
        for raw_rule_id, ground_truth_id
        in reverse_rule_mapping.items()
        if (
            clean_rule_id := normalise_rule_id(
                raw_rule_id
            )
        )
    }

    normalised: list[dict[str, Any]] = []

    for index, finding in enumerate(
        extracted_findings,
        start=1,
    ):
        rule_id = normalise_rule_id(
            finding.get("rule_id")
        )

        ground_truth_id = (
            cleaned_rule_mapping.get(rule_id)
            if rule_id is not None
            else None
        )

        ground_truth_item = (
            ground_truth_items.get(ground_truth_id)
            if ground_truth_id is not None
            else None
        )

        # Approved rule-ID mappings decide whether a scanner finding represents ground truth.
        mapping_status = (
            "mapped"
            if ground_truth_item is not None
            else "unmapped"
        )

        canonical_resource_name = None
        canonical_container = None

        if ground_truth_item is not None:
            (
                canonical_resource_name,
                canonical_container,
            ) = canonical_resource(
                ground_truth_item
            )

        # Ground truth supplies canonical comparison fields while original scanner values remain available.
        normalised_finding = {
            "finding_id": (
                f"{scanner}-{case_id}-{index:04d}"
            ),
            "tool": scanner,
            "case_id": case_id,
            "artifact_type": artifact_type,
            "rule_id": rule_id,
            "rule_name": finding.get("rule_name"),
            "status": finding.get("status"),
            "message": finding.get("message"),

            "category": (
                ground_truth_item.get("category")
                if ground_truth_item is not None
                else finding.get("original_category")
            ),

            "subcategory": (
                ground_truth_item.get("subcategory")
                if ground_truth_item is not None
                else finding.get(
                    "original_subcategory"
                )
            ),

            "severity": (
                ground_truth_item.get("severity")
                if ground_truth_item is not None
                else finding.get("severity")
            ),

            "resource": (
                canonical_resource_name
                or finding.get("resource")
            ),

            "container": (
                canonical_container
                or finding.get("container")
            ),

            "field_path": (
                ground_truth_item.get("field_path")
                if ground_truth_item is not None
                else finding.get("field_path")
            ),

            "bad_value": (
                ground_truth_item.get("bad_value")
                if ground_truth_item is not None
                else None
            ),

            "expected_secure_value": (
                ground_truth_item.get(
                    "expected_secure_value"
                )
                if ground_truth_item is not None
                else None
            ),

            "ground_truth_id": ground_truth_id,
            "mapping_status": mapping_status,

            "original_category": finding.get(
                "original_category"
            ),

            "original_subcategory": finding.get(
                "original_subcategory"
            ),

            "original_severity": finding.get(
                "severity"
            ),

            "original_resource": finding.get(
                "resource"
            ),

            "source_file": finding.get(
                "source_file"
            ),

            "line_start": finding.get(
                "line_start"
            ),

            "line_end": finding.get(
                "line_end"
            ),

            "failed_resources": finding.get(
                "failed_resources"
            ),

            "passed_resources": finding.get(
                "passed_resources"
            ),

            "skipped_resources": finding.get(
                "skipped_resources"
            ),

            "score": finding.get("score"),

            "compliance_score": finding.get(
                "compliance_score"
            ),
        }

        normalised.append(normalised_finding)

    return normalised


# This function writes formatted JSON output.
def write_output(
    output_path: Path,
    content: dict[str, Any],
) -> None:
    """Write formatted JSON output."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                content,
                file,
                indent=2,
                ensure_ascii=False,
            )

            file.write("\n")

    except OSError as error:
        raise NormalisationError(
            f"Could not write output file: {error}"
        ) from error


# This function reads command-line arguments.
def parse_arguments() -> argparse.Namespace:
    """Read command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Normalise Checkov, Trivy, or Kubescape "
            "findings using benchmark_config.yaml."
        )
    )

    parser.add_argument(
        "--case",
        required=True,
        dest="case_id",
        help="Benchmark case ID.",
    )

    parser.add_argument(
        "--scanner",
        required=True,
        choices=sorted(SUPPORTED_SCANNERS),
        help="Scanner whose raw output will be normalised.",
    )

    parser.add_argument(
        "--output-root",
        default="results/normalised_generic",
        help=(
            "Output root directory. The default avoids "
            "overwriting the existing normalised outputs."
        ),
    )

    return parser.parse_args()


# This function runs the generic normalisation pipeline.
def run() -> Path:
    """Run the generic normalisation pipeline."""

    arguments = parse_arguments()

    case_id = arguments.case_id.strip()
    scanner = arguments.scanner.strip().lower()

    configuration = load_benchmark_config()

    case_configuration = get_case_configuration(
        configuration,
        case_id,
    )

    ground_truth = load_case_ground_truth(
        case_configuration
    )

    ground_truth_items = get_ground_truth_items(
        ground_truth
    )

    reverse_rule_mapping = (
        build_rule_to_ground_truth_map(
            case_configuration,
            scanner,
        )
    )

    raw_path = (
        PROJECT_ROOT
        / "results"
        / "raw"
        / scanner
        / f"{case_id}.json"
    )

    raw_data = read_json(raw_path)

    extracted_findings = extract_scanner_findings(
        scanner,
        raw_data,
    )

    artifact_type = str(
        case_configuration.get(
            "artifact_type",
            ground_truth.get(
                "artifact_type",
                "unknown",
            ),
        )
    )

    findings = normalise_findings(
        scanner=scanner,
        case_id=case_id,
        artifact_type=artifact_type,
        extracted_findings=extracted_findings,
        reverse_rule_mapping=reverse_rule_mapping,
        ground_truth_items=ground_truth_items,
    )

    mapped_count = sum(
        finding.get("mapping_status") == "mapped"
        for finding in findings
    )

    unmapped_count = (
        len(findings) - mapped_count
    )

    output_root = (
        PROJECT_ROOT
        / arguments.output_root
    ).resolve()

    # Reject path traversal so generated results remain inside the project.
    try:
        output_root.relative_to(PROJECT_ROOT)

    except ValueError as error:
        raise NormalisationError(
            "The output directory must be inside "
            "the project directory."
        ) from error

    output_path = (
        output_root
        / scanner
        / f"{case_id}.normalised.json"
    )

    content = {
        "schema_version": "1.0",
        "case_id": case_id,
        "tool": scanner,
        "scanner_version": read_scanner_version(
            scanner
        ),
        "artifact_type": artifact_type,
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "source_file": str(
            raw_path.relative_to(PROJECT_ROOT)
        ),
        "summary": {
            "normalised_findings_count": len(
                findings
            ),
            "mapped_findings_count": mapped_count,
            "unmapped_findings_count": unmapped_count,
        },
        "findings": findings,
    }

    write_output(
        output_path,
        content,
    )

    print("Generic normalisation completed.")
    print(f"Case: {case_id}")
    print(f"Scanner: {scanner}")
    print(
        f"Normalised findings: {len(findings)}"
    )
    print(f"Mapped findings: {mapped_count}")
    print(f"Unmapped findings: {unmapped_count}")
    print(
        "Output: "
        f"{output_path.relative_to(PROJECT_ROOT)}"
    )

    return output_path


# This function serves as the application entry point and handles any errors.
def main() -> int:
    """Application entry point."""

    try:
        run()
        return 0

    except (
        ConfigurationError,
        NormalisationError,
    ) as error:
        print()
        print("Generic normalisation failed.")
        print(f"Reason: {error}")
        return 1

    except KeyboardInterrupt:
        print()
        print("Normalisation cancelled by the user.")
        return 130

    except Exception as error:
        print()
        print("Unexpected normalisation error.")
        print(
            f"{type(error).__name__}: {error}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
