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

SUPPORTED_MATCHING_MODES = {
    "review",
    "strict",
}


class ReportError(Exception):
    """Raised when a benchmark report cannot be generated."""


# This function reads a JSON file and confirms that its root is an object.
def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file and confirm that its root is an object."""

    if not path.exists():
        raise ReportError(
            f"Required input file does not exist: {path}"
        )

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ReportError(
            f"Invalid JSON in {path.name}: {error}"
        ) from error

    except OSError as error:
        raise ReportError(
            f"Could not read {path}: {error}"
        ) from error

    if not isinstance(data, dict):
        raise ReportError(
            f"The root of {path.name} must be a JSON object."
        )

    return data


# This function writes a UTF-8 text file.
def write_text(
    path: Path,
    content: str,
) -> None:
    """Write a UTF-8 text file."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        path.write_text(
            content,
            encoding="utf-8",
        )

    except OSError as error:
        raise ReportError(
            f"Could not write report: {error}"
        ) from error


# This function resolves a project-relative directory and prevents paths outside the benchmark project.
def resolve_internal_directory(
    directory_value: str,
    field_name: str,
) -> Path:
    """
    Resolve a project-relative directory and prevent paths
    outside the benchmark project.
    """

    directory = (
        PROJECT_ROOT
        / directory_value
    ).resolve()

    # Reject path traversal so input and output cannot escape the project directory.
    try:
        directory.relative_to(PROJECT_ROOT)

    except ValueError as error:
        raise ReportError(
            f"{field_name} must be inside the project directory."
        ) from error

    return directory


# This function retrieves and validates a list of JSON objects.
def get_object_list(
    document: dict[str, Any],
    field_name: str,
) -> list[dict[str, Any]]:
    """Retrieve and validate a list of JSON objects."""

    value = document.get(field_name)

    if not isinstance(value, list):
        raise ReportError(
            f"The matched file must contain a "
            f"'{field_name}' list."
        )

    validated_items: list[dict[str, Any]] = []

    for index, item in enumerate(
        value,
        start=1,
    ):
        if not isinstance(item, dict):
            raise ReportError(
                f"Item {index} in '{field_name}' "
                "is not a JSON object."
            )

        validated_items.append(item)

    return validated_items


# This function returns a stripped string or None.
def clean_text(value: Any) -> str | None:
    """Return a stripped string or None."""

    if not isinstance(value, str):
        return None

    cleaned_value = value.strip()

    return cleaned_value or None


# This function converts a value into readable report text.
def display_value(value: Any) -> str:
    """Convert a value into readable report text."""

    if value is None:
        return "—"

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, (dict, list)):
        return json.dumps(
            value,
            ensure_ascii=False,
        )

    text = str(value).strip()

    return text or "—"


# This function escapes a value for use inside a Markdown table.
def markdown_table_value(value: Any) -> str:
    """Escape a value for use inside a Markdown table."""

    text = display_value(value)

    text = text.replace(
        "\r\n",
        "\n",
    )

    text = text.replace(
        "\r",
        "\n",
    )

    text = text.replace(
        "\n",
        "<br>",
    )

    text = text.replace(
        "|",
        r"\|",
    )

    text = text.replace(
        "`",
        "'",
    )

    return text


# This function formats a metric value for the report.
def format_metric(value: Any) -> str:
    """Format a metric value for the report."""

    if value is None:
        return "Undefined"

    if isinstance(value, bool):
        return display_value(value)

    if isinstance(value, (int, float)):
        return f"{value:.4f}".rstrip("0").rstrip(".")

    return display_value(value)


# This function returns a presentation-friendly scanner name.
def scanner_display_name(scanner: str) -> str:
    """Return a presentation-friendly scanner name."""

    names = {
        "checkov": "Checkov",
        "trivy": "Trivy",
        "kubescape": "Kubescape",
    }

    return names.get(
        scanner,
        scanner.title(),
    )


# This function creates a readable resource identifier.
def format_ground_truth_resource(
    ground_truth_item: dict[str, Any],
) -> str:
    """Create a readable resource identifier."""

    resource = ground_truth_item.get("resource")

    if isinstance(resource, str):
        return resource

    if not isinstance(resource, dict):
        return "—"

    kind = resource.get("kind")
    namespace = resource.get(
        "namespace",
        "default",
    )
    name = resource.get("name")

    components = [
        str(value)
        for value in (
            kind,
            namespace,
            name,
        )
        if value is not None
        and str(value).strip()
    ]

    if not components:
        return "—"

    return ".".join(components)


# This function retrieves a container name from ground truth.
def get_ground_truth_container(
    ground_truth_item: dict[str, Any],
) -> Any:
    """Retrieve a container name from ground truth."""

    resource = ground_truth_item.get("resource")

    if isinstance(resource, dict):
        container = resource.get("container")

        if container is not None:
            return container

    return ground_truth_item.get("container")


# This function validates that matched and metrics files belong together.
def validate_documents(
    matched_document: dict[str, Any],
    metrics_document: dict[str, Any],
    expected_case_id: str,
    expected_scanner: str,
) -> str:
    """Validate that matched and metrics files belong together."""

    matched_case = matched_document.get("case_id")
    metrics_case = metrics_document.get("case_id")

    matched_scanner = matched_document.get("tool")
    metrics_scanner = metrics_document.get("tool")

    if matched_case != expected_case_id:
        raise ReportError(
            "The matched file case ID does not match "
            f"the requested case. Expected '{expected_case_id}', "
            f"found '{matched_case}'."
        )

    if metrics_case != expected_case_id:
        raise ReportError(
            "The metrics file case ID does not match "
            f"the requested case. Expected '{expected_case_id}', "
            f"found '{metrics_case}'."
        )

    if matched_scanner != expected_scanner:
        raise ReportError(
            "The matched file scanner does not match "
            f"the requested scanner. Expected "
            f"'{expected_scanner}', found '{matched_scanner}'."
        )

    if metrics_scanner != expected_scanner:
        raise ReportError(
            "The metrics file scanner does not match "
            f"the requested scanner. Expected "
            f"'{expected_scanner}', found '{metrics_scanner}'."
        )

    matched_mode = clean_text(
        matched_document.get("matching_mode")
    )

    metrics_mode = clean_text(
        metrics_document.get("matching_mode")
    )

    if matched_mode is None:
        raise ReportError(
            "The matched file has no valid matching_mode."
        )

    if metrics_mode is None:
        raise ReportError(
            "The metrics file has no valid matching_mode."
        )

    matched_mode = matched_mode.lower()
    metrics_mode = metrics_mode.lower()

    if matched_mode not in SUPPORTED_MATCHING_MODES:
        raise ReportError(
            "The matched file matching_mode must be "
            "'review' or 'strict'."
        )

    if metrics_mode not in SUPPORTED_MATCHING_MODES:
        raise ReportError(
            "The metrics file matching_mode must be "
            "'review' or 'strict'."
        )

    if matched_mode != metrics_mode:
        raise ReportError(
            "The matched and metrics files use different "
            f"matching modes: '{matched_mode}' and "
            f"'{metrics_mode}'."
        )

    return matched_mode


# This function confirms that matched and metrics counts agree.
def validate_count_consistency(
    matched_document: dict[str, Any],
    metrics_document: dict[str, Any],
) -> None:
    """Confirm that matched and metrics counts agree."""

    matched_counts = matched_document.get(
        "counts",
        {},
    )

    metrics_counts = metrics_document.get(
        "counts",
        {},
    )

    if not isinstance(matched_counts, dict):
        raise ReportError(
            "The matched file has no valid counts object."
        )

    if not isinstance(metrics_counts, dict):
        raise ReportError(
            "The metrics file has no valid counts object."
        )

    count_fields = [
        "total_normalised_findings",
        "ground_truth_issue_count",
        "true_positive_count",
        "false_positive_count",
        "false_negative_count",
        "unlabelled_extra_findings_count",
        "duplicate_match_count",
        "ambiguous_match_count",
    ]

    # Refuse to combine stale or unrelated stage outputs in one report.
    for field_name in count_fields:
        matched_value = matched_counts.get(
            field_name
        )

        metrics_value = metrics_counts.get(
            field_name
        )

        if matched_value != metrics_value:
            raise ReportError(
                "Matched and metrics counts disagree for "
                f"'{field_name}'. Matched file: "
                f"{matched_value}; metrics file: "
                f"{metrics_value}."
            )


# This function appends a Markdown table to the report.
def append_table(
    lines: list[str],
    headers: list[str],
    rows: list[list[Any]],
) -> None:
    """Append a Markdown table to the report."""

    lines.append(
        "| "
        + " | ".join(headers)
        + " |"
    )

    lines.append(
        "| "
        + " | ".join(
            "---"
            for _ in headers
        )
        + " |"
    )

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                markdown_table_value(value)
                for value in row
            )
            + " |"
        )

    lines.append("")


ColumnExtractor = Callable[
    [dict[str, Any]],
    Any,
]


# This function appends a finding classification section.
def append_finding_section(
    lines: list[str],
    title: str,
    introduction: str,
    findings: list[dict[str, Any]],
    columns: list[
        tuple[
            str,
            ColumnExtractor,
        ]
    ],
) -> None:
    """Append a finding classification section."""

    lines.append(f"## {title}")
    lines.append("")
    lines.append(introduction)
    lines.append("")

    if not findings:
        lines.append(
            "No findings were recorded in this category."
        )
        lines.append("")
        return

    headers = [
        heading
        for heading, _ in columns
    ]

    rows: list[list[Any]] = []

    for finding in findings:
        row = [
            extractor(finding)
            for _, extractor in columns
        ]

        rows.append(row)

    append_table(
        lines,
        headers,
        rows,
    )


# This function builds the ground-truth evaluation table.
def build_ground_truth_rows(
    ground_truth_items: dict[str, dict[str, Any]],
    true_positives: list[dict[str, Any]],
    duplicate_matches: list[dict[str, Any]],
) -> list[list[Any]]:
    """Build the ground-truth evaluation table."""

    detections: dict[
        str,
        list[dict[str, Any]],
    ] = {}

    for finding in (
        true_positives
        + duplicate_matches
    ):
        ground_truth_id = clean_text(
            finding.get("ground_truth_id")
        )

        if ground_truth_id is None:
            continue

        detections.setdefault(
            ground_truth_id,
            [],
        ).append(finding)

    rows: list[list[Any]] = []

    for (
        ground_truth_id,
        ground_truth_item,
    ) in ground_truth_items.items():
        related_findings = detections.get(
            ground_truth_id,
            [],
        )

        detected = bool(
            related_findings
        )

        rule_ids = sorted(
            {
                str(finding.get("rule_id"))
                for finding in related_findings
                if finding.get("rule_id")
            }
        )

        rows.append(
            [
                ground_truth_id,
                ground_truth_item.get(
                    "category"
                ),
                ground_truth_item.get(
                    "subcategory"
                ),
                ground_truth_item.get(
                    "severity"
                ),
                format_ground_truth_resource(
                    ground_truth_item
                ),
                get_ground_truth_container(
                    ground_truth_item
                ),
                ground_truth_item.get(
                    "field_path"
                ),
                (
                    "Detected"
                    if detected
                    else "Missed"
                ),
                (
                    ", ".join(rule_ids)
                    if rule_ids
                    else "—"
                ),
            ]
        )

    return rows


# This function creates the complete Markdown report.
def build_report(
    case_id: str,
    scanner: str,
    matching_mode: str,
    matched_document: dict[str, Any],
    metrics_document: dict[str, Any],
    ground_truth_items: dict[str, dict[str, Any]],
    matched_path: Path,
    metrics_path: Path,
) -> str:
    """Create the complete Markdown report."""

    true_positives = get_object_list(
        matched_document,
        "true_positives",
    )

    false_positives = get_object_list(
        matched_document,
        "false_positives",
    )

    false_negatives = get_object_list(
        matched_document,
        "false_negatives",
    )

    unlabelled_extras = get_object_list(
        matched_document,
        "unlabelled_extras",
    )

    duplicate_matches = get_object_list(
        matched_document,
        "duplicate_matches",
    )

    ambiguous_matches = get_object_list(
        matched_document,
        "ambiguous_matches",
    )

    counts = metrics_document.get(
        "counts",
        {},
    )

    metrics = metrics_document.get(
        "metrics",
        {},
    )

    formula_used = metrics_document.get(
        "formula_used",
        {},
    )

    interpretation = metrics_document.get(
        "interpretation",
        {},
    )

    if not isinstance(counts, dict):
        raise ReportError(
            "The metrics file has no valid counts object."
        )

    if not isinstance(metrics, dict):
        raise ReportError(
            "The metrics file has no valid metrics object."
        )

    if not isinstance(formula_used, dict):
        formula_used = {}

    if not isinstance(interpretation, dict):
        interpretation = {}

    generated_at = datetime.now(
        timezone.utc
    ).isoformat()

    scanner_name = scanner_display_name(
        scanner
    )

    evaluation_status = metrics_document.get(
        "evaluation_status",
        "unknown",
    )

    scanner_version = (
        metrics_document.get("scanner_version")
        or matched_document.get("scanner_version")
        or "Unknown"
    )

    scanner_version_text = display_value(
        scanner_version
    ).replace(
        "```",
        "'''",
    )

    lines: list[str] = []

    lines.append(
        f"# Benchmark Report: {scanner_name}"
    )
    lines.append("")
    lines.append(
        f"**Case:** `{case_id}`"
    )
    lines.append("")

    lines.append("## Benchmark information")
    lines.append("")

    append_table(
        lines,
        [
            "Property",
            "Value",
        ],
        [
            [
                "Case ID",
                case_id,
            ],
            [
                "Scanner",
                scanner_name,
            ],
            [
                "Artifact type",
                matched_document.get(
                    "artifact_type"
                ),
            ],
            [
                "Matching mode",
                matching_mode,
            ],
            [
                "Evaluation status",
                evaluation_status,
            ],
            [
                "Report generated",
                generated_at,
            ],
        ],
    )

    lines.append("### Scanner version")
    lines.append("")
    lines.append("```text")
    lines.append(scanner_version_text)
    lines.append("```")
    lines.append("")

    lines.append("## Results summary")
    lines.append("")

    append_table(
        lines,
        [
            "Measure",
            "Count",
        ],
        [
            [
                "Normalised findings",
                counts.get(
                    "total_normalised_findings"
                ),
            ],
            [
                "Ground-truth issues",
                counts.get(
                    "ground_truth_issue_count"
                ),
            ],
            [
                "True positives",
                counts.get(
                    "true_positive_count"
                ),
            ],
            [
                "False positives",
                counts.get(
                    "false_positive_count"
                ),
            ],
            [
                "False negatives",
                counts.get(
                    "false_negative_count"
                ),
            ],
            [
                "Unlabelled extras",
                counts.get(
                    "unlabelled_extra_findings_count"
                ),
            ],
            [
                "Duplicate matches",
                counts.get(
                    "duplicate_match_count"
                ),
            ],
            [
                "Ambiguous matches",
                counts.get(
                    "ambiguous_match_count"
                ),
            ],
        ],
    )

    lines.append("## Performance metrics")
    lines.append("")

    append_table(
        lines,
        [
            "Metric",
            "Formula",
            "Result",
        ],
        [
            [
                "Precision",
                formula_used.get(
                    "precision",
                    "TP / (TP + FP)",
                ),
                format_metric(
                    metrics.get("precision")
                ),
            ],
            [
                "Recall",
                formula_used.get(
                    "recall",
                    "TP / (TP + FN)",
                ),
                format_metric(
                    metrics.get("recall")
                ),
            ],
            [
                "F1 score",
                formula_used.get(
                    "f1_score",
                    (
                        "2 × (Precision × Recall) "
                        "/ (Precision + Recall)"
                    ),
                ),
                format_metric(
                    metrics.get("f1_score")
                ),
            ],
        ],
    )

    lines.append("## Ground-truth evaluation")
    lines.append("")
    lines.append(
        "This table shows whether each known benchmark "
        "issue was detected by the scanner."
    )
    lines.append("")

    ground_truth_rows = build_ground_truth_rows(
        ground_truth_items=ground_truth_items,
        true_positives=true_positives,
        duplicate_matches=duplicate_matches,
    )

    append_table(
        lines,
        [
            "Ground truth",
            "Category",
            "Subcategory",
            "Severity",
            "Resource",
            "Container",
            "Field path",
            "Result",
            "Scanner rule",
        ],
        ground_truth_rows,
    )

    append_finding_section(
        lines=lines,
        title="True positives",
        introduction=(
            "These findings correctly matched a known "
            "ground-truth issue."
        ),
        findings=true_positives,
        columns=[
            (
                "Finding",
                lambda item: item.get(
                    "finding_id"
                ),
            ),
            (
                "Rule",
                lambda item: item.get(
                    "rule_id"
                ),
            ),
            (
                "Rule name",
                lambda item: item.get(
                    "rule_name"
                ),
            ),
            (
                "Ground truth",
                lambda item: item.get(
                    "ground_truth_id"
                ),
            ),
            (
                "Severity",
                lambda item: item.get(
                    "severity"
                ),
            ),
            (
                "Resource",
                lambda item: item.get(
                    "resource"
                ),
            ),
            (
                "Container",
                lambda item: item.get(
                    "container"
                ),
            ),
            (
                "Field path",
                lambda item: item.get(
                    "field_path"
                ),
            ),
        ],
    )

    append_finding_section(
        lines=lines,
        title="False positives",
        introduction=(
            "These findings were classified as incorrect "
            "according to the selected matching policy."
        ),
        findings=false_positives,
        columns=[
            (
                "Finding",
                lambda item: item.get(
                    "finding_id"
                ),
            ),
            (
                "Rule",
                lambda item: item.get(
                    "rule_id"
                ),
            ),
            (
                "Rule name",
                lambda item: item.get(
                    "rule_name"
                ),
            ),
            (
                "Severity",
                lambda item: item.get(
                    "severity"
                ),
            ),
            (
                "Resource",
                lambda item: item.get(
                    "resource"
                ),
            ),
            (
                "Reason",
                lambda item: item.get(
                    "classification_reason"
                ),
            ),
        ],
    )

    append_finding_section(
        lines=lines,
        title="False negatives",
        introduction=(
            "These ground-truth issues were not detected "
            "by the scanner."
        ),
        findings=false_negatives,
        columns=[
            (
                "Ground truth",
                lambda item: item.get(
                    "ground_truth_id"
                ),
            ),
            (
                "Category",
                lambda item: item.get(
                    "category"
                ),
            ),
            (
                "Subcategory",
                lambda item: item.get(
                    "subcategory"
                ),
            ),
            (
                "Severity",
                lambda item: item.get(
                    "severity"
                ),
            ),
            (
                "Resource",
                lambda item: item.get(
                    "resource"
                ),
            ),
            (
                "Container",
                lambda item: item.get(
                    "container"
                ),
            ),
            (
                "Field path",
                lambda item: item.get(
                    "field_path"
                ),
            ),
        ],
    )

    append_finding_section(
        lines=lines,
        title="Unlabelled extra findings",
        introduction=(
            "These scanner findings do not yet have an "
            "approved mapping to the benchmark ground truth."
        ),
        findings=unlabelled_extras,
        columns=[
            (
                "Finding",
                lambda item: item.get(
                    "finding_id"
                ),
            ),
            (
                "Rule",
                lambda item: item.get(
                    "rule_id"
                ),
            ),
            (
                "Rule name",
                lambda item: item.get(
                    "rule_name"
                ),
            ),
            (
                "Severity",
                lambda item: item.get(
                    "severity"
                ),
            ),
            (
                "Original category",
                lambda item: item.get(
                    "original_category"
                ),
            ),
            (
                "Original subcategory",
                lambda item: item.get(
                    "original_subcategory"
                ),
            ),
            (
                "Resource",
                lambda item: item.get(
                    "original_resource"
                )
                or item.get("resource"),
            ),
        ],
    )

    append_finding_section(
        lines=lines,
        title="Duplicate matches",
        introduction=(
            "These additional findings matched an issue "
            "that had already been counted as a true positive."
        ),
        findings=duplicate_matches,
        columns=[
            (
                "Finding",
                lambda item: item.get(
                    "finding_id"
                ),
            ),
            (
                "Rule",
                lambda item: item.get(
                    "rule_id"
                ),
            ),
            (
                "Rule name",
                lambda item: item.get(
                    "rule_name"
                ),
            ),
            (
                "Ground truth",
                lambda item: item.get(
                    "ground_truth_id"
                ),
            ),
            (
                "Reason",
                lambda item: item.get(
                    "classification_reason"
                ),
            ),
        ],
    )

    append_finding_section(
        lines=lines,
        title="Ambiguous matches",
        introduction=(
            "These findings contained incomplete or "
            "inconsistent mapping information."
        ),
        findings=ambiguous_matches,
        columns=[
            (
                "Finding",
                lambda item: item.get(
                    "finding_id"
                ),
            ),
            (
                "Rule",
                lambda item: item.get(
                    "rule_id"
                ),
            ),
            (
                "Rule name",
                lambda item: item.get(
                    "rule_name"
                ),
            ),
            (
                "Ground truth",
                lambda item: item.get(
                    "ground_truth_id"
                ),
            ),
            (
                "Mapping status",
                lambda item: item.get(
                    "mapping_status"
                ),
            ),
            (
                "Reason",
                lambda item: item.get(
                    "classification_reason"
                ),
            ),
        ],
    )

    lines.append(
        "## Interpretation and methodological notes"
    )
    lines.append("")

    precision_explanation = interpretation.get(
        "precision"
    )

    recall_explanation = interpretation.get(
        "recall"
    )

    f1_explanation = interpretation.get(
        "f1_score"
    )

    if precision_explanation:
        lines.append(
            f"- **Precision:** "
            f"{precision_explanation}"
        )

    if recall_explanation:
        lines.append(
            f"- **Recall:** "
            f"{recall_explanation}"
        )

    if f1_explanation:
        lines.append(
            f"- **F1 score:** "
            f"{f1_explanation}"
        )

    if matching_mode == "review":
        lines.append(
            "- **Review-mode policy:** Unmapped findings "
            "are retained as unlabelled extras. They are "
            "not counted as false positives until they "
            "have been manually reviewed."
        )

    if matching_mode == "strict":
        lines.append(
            "- **Strict-mode policy:** Unmapped findings "
            "are counted as false positives."
        )

    lines.append(
        "- **Duplicate policy:** Only the first valid "
        "finding mapped to a ground-truth issue is counted "
        "as a true positive. Additional detections of the "
        "same issue are stored as duplicate matches."
    )

    lines.append(
        "- **Ambiguous findings:** Ambiguous matches are "
        "reported separately and are excluded from the "
        "precision, recall and F1 calculations."
    )

    unlabelled_count = counts.get(
        "unlabelled_extra_findings_count",
        0,
    )

    if (
        matching_mode == "review"
        and isinstance(unlabelled_count, int)
        and unlabelled_count > 0
    ):
        lines.append(
            f"- **Current limitation:** The scanner "
            f"reported {unlabelled_count} unlabelled extra "
            "finding(s). Therefore, the reported precision "
            "only reflects the currently labelled portion "
            "of the benchmark results."
        )

    lines.append("")

    lines.append("## Input provenance")
    lines.append("")

    append_table(
        lines,
        [
            "Input",
            "Path",
            "Generated at",
        ],
        [
            [
                "Matched findings",
                str(
                    matched_path.relative_to(
                        PROJECT_ROOT
                    )
                ),
                matched_document.get(
                    "generated_at"
                ),
            ],
            [
                "Metrics",
                str(
                    metrics_path.relative_to(
                        PROJECT_ROOT
                    )
                ),
                metrics_document.get(
                    "generated_at"
                ),
            ],
        ],
    )

    lines.append("---")
    lines.append("")
    lines.append(
        "Report generated by the generic scanner "
        "benchmark reporting pipeline."
    )
    lines.append("")

    return "\n".join(lines)


# This function reads command-line arguments.
def parse_arguments() -> argparse.Namespace:
    """Read command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Generate a Markdown benchmark report from "
            "generic matched findings and metrics."
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
        help="Scanner whose report will be generated.",
    )

    parser.add_argument(
        "--matched-root",
        default="results/matched_generic",
        help=(
            "Directory containing generic matched results."
        ),
    )

    parser.add_argument(
        "--metrics-root",
        default="results/metrics_generic",
        help=(
            "Directory containing generic metrics results."
        ),
    )

    parser.add_argument(
        "--output-root",
        default="results/reports_generic",
        help=(
            "Directory where Markdown reports will be saved."
        ),
    )

    return parser.parse_args()


# This function runs the generic report-generation process.
def run() -> Path:
    """Run the generic report-generation process."""

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

    matched_root = resolve_internal_directory(
        arguments.matched_root,
        "Matched root",
    )

    metrics_root = resolve_internal_directory(
        arguments.metrics_root,
        "Metrics root",
    )

    output_root = resolve_internal_directory(
        arguments.output_root,
        "Output root",
    )

    matched_path = (
        matched_root
        / scanner
        / f"{case_id}.matched.json"
    )

    metrics_path = (
        metrics_root
        / scanner
        / f"{case_id}.metrics.json"
    )

    matched_document = read_json(
        matched_path
    )

    metrics_document = read_json(
        metrics_path
    )

    matching_mode = validate_documents(
        matched_document=matched_document,
        metrics_document=metrics_document,
        expected_case_id=case_id,
        expected_scanner=scanner,
    )

    validate_count_consistency(
        matched_document=matched_document,
        metrics_document=metrics_document,
    )

    report_content = build_report(
        case_id=case_id,
        scanner=scanner,
        matching_mode=matching_mode,
        matched_document=matched_document,
        metrics_document=metrics_document,
        ground_truth_items=ground_truth_items,
        matched_path=matched_path,
        metrics_path=metrics_path,
    )

    output_path = (
        output_root
        / scanner
        / f"{case_id}.report.md"
    )

    write_text(
        output_path,
        report_content,
    )

    counts = metrics_document.get(
        "counts",
        {},
    )

    metrics = metrics_document.get(
        "metrics",
        {},
    )

    if not isinstance(counts, dict):
        counts = {}

    if not isinstance(metrics, dict):
        metrics = {}

    print("Generic benchmark report generated.")
    print(f"Case: {case_id}")
    print(f"Scanner: {scanner}")
    print(f"Matching mode: {matching_mode}")
    print(
        "True positives: "
        f"{counts.get('true_positive_count')}"
    )
    print(
        "False positives: "
        f"{counts.get('false_positive_count')}"
    )
    print(
        "False negatives: "
        f"{counts.get('false_negative_count')}"
    )
    print(
        "Unlabelled extras: "
        f"{counts.get('unlabelled_extra_findings_count')}"
    )
    print(
        "Precision: "
        f"{format_metric(metrics.get('precision'))}"
    )
    print(
        "Recall: "
        f"{format_metric(metrics.get('recall'))}"
    )
    print(
        "F1 score: "
        f"{format_metric(metrics.get('f1_score'))}"
    )
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
        ReportError,
    ) as error:
        print()
        print("Generic report generation failed.")
        print(f"Reason: {error}")
        return 1

    except KeyboardInterrupt:
        print()
        print("Report generation cancelled.")
        return 130

    except Exception as error:
        print()
        print("Unexpected report-generation error.")
        print(
            f"{type(error).__name__}: {error}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
