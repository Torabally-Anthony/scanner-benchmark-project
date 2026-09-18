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
            "'strict'."
        )

    if metrics_mode not in SUPPORTED_MATCHING_MODES:
        raise ReportError(
            "The metrics file matching_mode must be "
            "'strict'."
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


# Keep Markdown readable; the matched JSON contains every finding and field.
FINDING_PREVIEW_LIMIT = 5


def append_finding_preview(
    lines: list[str],
    title: str,
    findings: list[dict[str, Any]],
    columns: list[tuple[str, Callable[[dict[str, Any]], Any]]],
) -> None:
    """Show a small sample of a non-empty finding category."""

    if not findings:
        return

    lines.extend([f"## {title} ({len(findings)})", ""])
    append_table(
        lines,
        [heading for heading, _ in columns],
        [
            [extractor(finding) for _, extractor in columns]
            for finding in findings[:FINDING_PREVIEW_LIMIT]
        ],
    )

    remaining = len(findings) - FINDING_PREVIEW_LIMIT
    if remaining > 0:
        lines.extend([
            f"Showing {FINDING_PREVIEW_LIMIT} of {len(findings)}. "
            "See the matched JSON for the full list.",
            "",
        ])


def build_ground_truth_rows(
    ground_truth_items: dict[str, dict[str, Any]],
    true_positives: list[dict[str, Any]],
    duplicate_matches: list[dict[str, Any]],
) -> list[list[Any]]:
    """Summarise the result for each benchmark issue."""

    detections: dict[str, set[str]] = {}
    for finding in true_positives + duplicate_matches:
        ground_truth_id = clean_text(finding.get("ground_truth_id"))
        if ground_truth_id:
            rule_id = clean_text(finding.get("rule_id"))
            detections.setdefault(ground_truth_id, set())
            if rule_id:
                detections[ground_truth_id].add(rule_id)

    return [
        [
            ground_truth_id,
            item.get("subcategory") or item.get("category"),
            format_ground_truth_resource(item),
            "Detected" if ground_truth_id in detections else "Missed",
            ", ".join(sorted(detections.get(ground_truth_id, set()))) or "—",
        ]
        for ground_truth_id, item in ground_truth_items.items()
    ]


# This function creates a compact Markdown report; JSON retains full detail.
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
    """Create a concise, reviewable Markdown report."""

    findings = {
        "True positives": get_object_list(matched_document, "true_positives"),
        "False positives": get_object_list(matched_document, "false_positives"),
        "False negatives": get_object_list(matched_document, "false_negatives"),
        "Unlabelled extras": get_object_list(matched_document, "unlabelled_extras"),
        "Duplicate matches": get_object_list(matched_document, "duplicate_matches"),
        "Ambiguous matches": get_object_list(matched_document, "ambiguous_matches"),
    }
    counts = metrics_document.get("counts")
    metrics = metrics_document.get("metrics")
    formulas = metrics_document.get("formula_used")
    if not isinstance(counts, dict):
        raise ReportError("The metrics file has no valid counts object.")
    if not isinstance(metrics, dict):
        raise ReportError("The metrics file has no valid metrics object.")
    if not isinstance(formulas, dict):
        formulas = {}

    version = (
        metrics_document.get("scanner_version")
        or matched_document.get("scanner_version")
        or "Unknown"
    )
    version = display_value(version).splitlines()[0].removeprefix(
        "Your current version is: "
    )
    generated_at = datetime.now(timezone.utc).isoformat()
    lines = [
        f"# Benchmark Report: {scanner_display_name(scanner)}",
        "",
        f"**Case:** `{case_id}`",
        "",
        (
            f"Artifact: `{markdown_table_value(matched_document.get('artifact_type'))}`"
            f" · Mode: `{matching_mode}`"
            f" · Status: `{markdown_table_value(metrics_document.get('evaluation_status'))}`"
        ),
        "",
    ]
    if version != "Unknown":
        lines.extend([f"Scanner version: `{markdown_table_value(version)}`", ""])

    lines.extend(["## Results summary", ""])
    append_table(
        lines,
        ["Measure", "Count"],
        [
            [label, counts.get(key)]
            for label, key in [
                ("Normalised findings", "total_normalised_findings"),
                ("Ground-truth issues", "ground_truth_issue_count"),
                ("True positives", "true_positive_count"),
                ("False positives", "false_positive_count"),
                ("False negatives", "false_negative_count"),
                ("Unlabelled extras", "unlabelled_extra_findings_count"),
                ("Duplicate matches", "duplicate_match_count"),
                ("Ambiguous matches", "ambiguous_match_count"),
            ]
        ],
    )

    lines.extend(["## Performance metrics", ""])
    append_table(
        lines,
        ["Metric", "Formula", "Result"],
        [
            ["Precision", formulas.get("precision", "TP / (TP + FP)"),
             format_metric(metrics.get("precision"))],
            ["Recall", formulas.get("recall", "TP / (TP + FN)"),
             format_metric(metrics.get("recall"))],
            ["F1 score", formulas.get("f1_score", "2PR / (P + R)"),
             format_metric(metrics.get("f1_score"))],
        ],
    )

    lines.extend(["## Ground-truth evaluation", ""])
    append_table(
        lines,
        ["Ground truth", "Issue", "Resource", "Result", "Scanner rule"],
        build_ground_truth_rows(
            ground_truth_items,
            findings["True positives"],
            findings["Duplicate matches"],
        ),
    )

    finding_id = lambda item: item.get("finding_id")
    rule_id = lambda item: item.get("rule_id")
    ground_truth_id = lambda item: item.get("ground_truth_id")
    resource = lambda item: item.get("resource") or item.get("original_resource")
    for title, columns in [
        ("True positives", [
            ("Finding", finding_id), ("Rule", rule_id),
            ("Ground truth", ground_truth_id), ("Resource", resource),
        ]),
        ("False positives", [
            ("Finding", finding_id), ("Rule", rule_id),
            ("Resource", resource),
        ]),
        ("False negatives", [
            ("Ground truth", ground_truth_id),
            ("Issue", lambda item: item.get("subcategory") or item.get("category")),
            ("Resource", resource),
        ]),
        ("Unlabelled extras", [
            ("Finding", finding_id), ("Rule", rule_id),
            ("Resource", resource),
        ]),
        ("Duplicate matches", [
            ("Finding", finding_id), ("Rule", rule_id),
            ("Ground truth", ground_truth_id),
        ]),
        ("Ambiguous matches", [
            ("Finding", finding_id), ("Rule", rule_id),
            ("Ground truth", ground_truth_id),
            ("Mapping status", lambda item: item.get("mapping_status")),
        ]),
    ]:
        append_finding_preview(lines, title, findings[title], columns)

    lines.extend([
        "Unmapped findings count as false positives; duplicate and ambiguous "
        "matches are excluded from the scores.",
        "",
        "- Full findings: `" + str(matched_path.relative_to(PROJECT_ROOT)) + "`",
        "- Full metrics: `" + str(metrics_path.relative_to(PROJECT_ROOT)) + "`",
        "- Generated: `" + generated_at + "`",
        "",
    ])
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
