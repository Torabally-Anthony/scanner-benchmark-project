from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
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
    "kubescape",
}

SUPPORTED_MATCHING_MODES = {
    "review",
    "strict",
}


class MetricsError(Exception):
    """Raised when benchmark metrics cannot be calculated."""


# This function reads a JSON file and confirms that its root is an object.
def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file and confirm that its root is an object."""

    if not path.exists():
        raise MetricsError(
            f"Matched findings file does not exist: {path}"
        )

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise MetricsError(
            f"Invalid JSON in {path.name}: {error}"
        ) from error

    except OSError as error:
        raise MetricsError(
            f"Could not read {path}: {error}"
        ) from error

    if not isinstance(data, dict):
        raise MetricsError(
            f"The root of {path.name} must be a JSON object."
        )

    return data


# This function writes formatted JSON output.
def write_json(
    path: Path,
    content: dict[str, Any],
) -> None:
    """Write formatted JSON output."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        with path.open(
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
        raise MetricsError(
            f"Could not write metrics output: {error}"
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
        raise MetricsError(
            f"{field_name} must be inside the project directory."
        ) from error

    return directory


# This function retrieves and validates a classification list.
def get_list(
    document: dict[str, Any],
    field_name: str,
) -> list[dict[str, Any]]:
    """Retrieve and validate a classification list."""

    value = document.get(field_name)

    if not isinstance(value, list):
        raise MetricsError(
            f"The matched file must contain a "
            f"'{field_name}' list."
        )

    validated_items: list[dict[str, Any]] = []

    for index, item in enumerate(
        value,
        start=1,
    ):
        if not isinstance(item, dict):
            raise MetricsError(
                f"Item {index} in '{field_name}' "
                "is not a JSON object."
            )

        validated_items.append(item)

    return validated_items


# This function divides two values safely.
def safe_divide(
    numerator: int,
    denominator: int,
) -> float | None:
    """
    Divide two values safely.

    None is returned when the denominator is zero because
    the metric is undefined.
    """

    # No observations means the metric is undefined, not automatically zero.
    if denominator == 0:
        return None

    return numerator / denominator


# This function calculates precision.
def calculate_precision(
    true_positive_count: int,
    false_positive_count: int,
) -> float | None:
    """Calculate precision."""

    return safe_divide(
        true_positive_count,
        true_positive_count + false_positive_count,
    )


# This function calculates recall.
def calculate_recall(
    true_positive_count: int,
    false_negative_count: int,
) -> float | None:
    """Calculate recall."""

    return safe_divide(
        true_positive_count,
        true_positive_count + false_negative_count,
    )


# This function calculates the F1 score.
def calculate_f1_score(
    precision: float | None,
    recall: float | None,
) -> float | None:
    """Calculate the F1 score."""

    if precision is None or recall is None:
        return None

    denominator = precision + recall

    if denominator == 0:
        return 0.0

    return (
        2
        * precision
        * recall
        / denominator
    )


# This function rounds a metric while preserving undefined values.
def round_metric(
    value: float | None,
    decimal_places: int,
) -> float | None:
    """Round a metric while preserving undefined values."""

    if value is None:
        return None

    return round(
        value,
        decimal_places,
    )


# This function validates the main matched-document properties.
def validate_matched_document(
    document: dict[str, Any],
    expected_case_id: str,
    expected_scanner: str,
) -> str:
    """Validate the main matched-document properties."""

    document_case_id = document.get("case_id")
    document_scanner = document.get("tool")
    matching_mode = document.get("matching_mode")

    if document_case_id != expected_case_id:
        raise MetricsError(
            "The matched file case ID does not match "
            f"the requested case. Expected '{expected_case_id}', "
            f"found '{document_case_id}'."
        )

    if document_scanner != expected_scanner:
        raise MetricsError(
            "The matched file scanner does not match "
            f"the requested scanner. Expected '{expected_scanner}', "
            f"found '{document_scanner}'."
        )

    if not isinstance(matching_mode, str):
        raise MetricsError(
            "The matched file does not contain a valid "
            "matching_mode."
        )

    matching_mode = matching_mode.strip().lower()

    if matching_mode not in SUPPORTED_MATCHING_MODES:
        raise MetricsError(
            "The matched file matching_mode must be "
            "'review' or 'strict'."
        )

    return matching_mode


# This function creates explanations for defined and undefined metrics.
def create_metric_explanations(
    true_positive_count: int,
    false_positive_count: int,
    false_negative_count: int,
    precision: float | None,
    recall: float | None,
    f1_score: float | None,
) -> dict[str, str]:
    """Create explanations for defined and undefined metrics."""

    precision_denominator = (
        true_positive_count
        + false_positive_count
    )

    recall_denominator = (
        true_positive_count
        + false_negative_count
    )

    if precision is None:
        precision_explanation = (
            "Precision is undefined because there were no "
            "true-positive or false-positive findings."
        )
    else:
        precision_explanation = (
            "Precision measures the proportion of classified "
            "positive findings that were true positives."
        )

    if recall is None:
        recall_explanation = (
            "Recall is undefined because there were no "
            "ground-truth positive issues to evaluate."
        )
    else:
        recall_explanation = (
            "Recall measures the proportion of ground-truth "
            "issues detected by the scanner."
        )

    if f1_score is None:
        f1_explanation = (
            "F1 is undefined because precision or recall "
            "is undefined."
        )
    else:
        f1_explanation = (
            "F1 is the harmonic mean of precision and recall."
        )

    return {
        "precision": precision_explanation,
        "recall": recall_explanation,
        "f1_score": f1_explanation,
        "precision_denominator": (
            f"TP + FP = {precision_denominator}"
        ),
        "recall_denominator": (
            f"TP + FN = {recall_denominator}"
        ),
    }


# This function reads command-line arguments.
def parse_arguments() -> argparse.Namespace:
    """Read command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Calculate precision, recall and F1 from "
            "generic matched benchmark results."
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
        help="Scanner whose metrics will be calculated.",
    )

    parser.add_argument(
        "--input-root",
        default="results/matched_generic",
        help=(
            "Directory containing generic matched results."
        ),
    )

    parser.add_argument(
        "--output-root",
        default="results/metrics_generic",
        help=(
            "Directory where generic metrics will be saved."
        ),
    )

    parser.add_argument(
        "--decimal-places",
        type=int,
        default=4,
        help=(
            "Number of decimal places used for metrics."
        ),
    )

    return parser.parse_args()


# This function runs the generic metric-calculation process.
def run() -> Path:
    """Run the generic metric-calculation process."""

    arguments = parse_arguments()

    case_id = arguments.case_id.strip()
    scanner = arguments.scanner.strip().lower()

    if arguments.decimal_places < 0:
        raise MetricsError(
            "Decimal places cannot be negative."
        )

    configuration = load_benchmark_config()

    # This confirms that the requested case is registered
    # in benchmark_config.yaml.
    get_case_configuration(
        configuration,
        case_id,
    )

    input_root = resolve_internal_directory(
        arguments.input_root,
        "Input root",
    )

    output_root = resolve_internal_directory(
        arguments.output_root,
        "Output root",
    )

    input_path = (
        input_root
        / scanner
        / f"{case_id}.matched.json"
    )

    matched_document = read_json(
        input_path
    )

    matching_mode = validate_matched_document(
        document=matched_document,
        expected_case_id=case_id,
        expected_scanner=scanner,
    )

    true_positives = get_list(
        matched_document,
        "true_positives",
    )

    false_positives = get_list(
        matched_document,
        "false_positives",
    )

    false_negatives = get_list(
        matched_document,
        "false_negatives",
    )

    unlabelled_extras = get_list(
        matched_document,
        "unlabelled_extras",
    )

    duplicate_matches = get_list(
        matched_document,
        "duplicate_matches",
    )

    ambiguous_matches = get_list(
        matched_document,
        "ambiguous_matches",
    )

    # Only TP, FP, and FN enter the formulas; extras, duplicates, and ambiguous matches are reported separately.
    true_positive_count = len(
        true_positives
    )

    false_positive_count = len(
        false_positives
    )

    false_negative_count = len(
        false_negatives
    )

    unlabelled_extra_count = len(
        unlabelled_extras
    )

    duplicate_match_count = len(
        duplicate_matches
    )

    ambiguous_match_count = len(
        ambiguous_matches
    )

    source_counts = matched_document.get(
        "counts",
        {},
    )

    if not isinstance(source_counts, dict):
        source_counts = {}

    total_normalised_findings = source_counts.get(
        "total_normalised_findings"
    )

    ground_truth_issue_count = source_counts.get(
        "ground_truth_issue_count"
    )

    if not isinstance(
        total_normalised_findings,
        int,
    ):
        total_normalised_findings = (
            true_positive_count
            + false_positive_count
            + unlabelled_extra_count
            + duplicate_match_count
            + ambiguous_match_count
        )

    if not isinstance(
        ground_truth_issue_count,
        int,
    ):
        ground_truth_issue_count = (
            true_positive_count
            + false_negative_count
        )

    classified_normalised_count = (
        true_positive_count
        + false_positive_count
        + unlabelled_extra_count
        + duplicate_match_count
        + ambiguous_match_count
    )

    if (
        classified_normalised_count
        != total_normalised_findings
    ):
        raise MetricsError(
            "The classification counts do not equal the "
            "total number of normalised findings. "
            f"Classified: {classified_normalised_count}; "
            f"expected: {total_normalised_findings}."
        )

    evaluated_ground_truth_count = (
        true_positive_count
        + false_negative_count
    )

    if (
        evaluated_ground_truth_count
        != ground_truth_issue_count
    ):
        raise MetricsError(
            "The true-positive and false-negative counts "
            "do not equal the ground-truth issue count. "
            f"Evaluated: {evaluated_ground_truth_count}; "
            f"expected: {ground_truth_issue_count}."
        )

    precision_raw = calculate_precision(
        true_positive_count,
        false_positive_count,
    )

    recall_raw = calculate_recall(
        true_positive_count,
        false_negative_count,
    )

    f1_raw = calculate_f1_score(
        precision_raw,
        recall_raw,
    )

    precision = round_metric(
        precision_raw,
        arguments.decimal_places,
    )

    recall = round_metric(
        recall_raw,
        arguments.decimal_places,
    )

    f1_score = round_metric(
        f1_raw,
        arguments.decimal_places,
    )

    explanations = create_metric_explanations(
        true_positive_count=true_positive_count,
        false_positive_count=false_positive_count,
        false_negative_count=false_negative_count,
        precision=precision,
        recall=recall,
        f1_score=f1_score,
    )

    requires_manual_review = (
        ambiguous_match_count > 0
        or (
            matching_mode == "review"
            and unlabelled_extra_count > 0
        )
    )

    evaluation_status = (
        "requires_manual_review"
        if requires_manual_review
        else "complete"
    )

    output_path = (
        output_root
        / scanner
        / f"{case_id}.metrics.json"
    )

    output_document = {
        "schema_version": "1.0",
        "case_id": case_id,
        "tool": scanner,
        "scanner_version": matched_document.get(
            "scanner_version"
        ),
        "artifact_type": matched_document.get(
            "artifact_type"
        ),
        "matching_mode": matching_mode,
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "source_file": str(
            input_path.relative_to(PROJECT_ROOT)
        ),

        "evaluation_status": evaluation_status,

        "counts": {
            "total_normalised_findings": (
                total_normalised_findings
            ),
            "ground_truth_issue_count": (
                ground_truth_issue_count
            ),
            "true_positive_count": (
                true_positive_count
            ),
            "false_positive_count": (
                false_positive_count
            ),
            "false_negative_count": (
                false_negative_count
            ),
            "unlabelled_extra_findings_count": (
                unlabelled_extra_count
            ),
            "duplicate_match_count": (
                duplicate_match_count
            ),
            "ambiguous_match_count": (
                ambiguous_match_count
            ),
        },

        "metrics": {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
        },

        "formula_used": {
            "precision": "TP / (TP + FP)",
            "recall": "TP / (TP + FN)",
            "f1_score": (
                "2 * (Precision * Recall) "
                "/ (Precision + Recall)"
            ),
        },

        "metric_inputs": {
            "precision": {
                "true_positives": (
                    true_positive_count
                ),
                "false_positives": (
                    false_positive_count
                ),
            },
            "recall": {
                "true_positives": (
                    true_positive_count
                ),
                "false_negatives": (
                    false_negative_count
                ),
            },
        },

        "interpretation": {
            **explanations,

            "review_mode_note": (
                "In review mode, unmapped findings are "
                "stored as unlabelled extras and are not "
                "counted as false positives."
            ),

            "strict_mode_note": (
                "In strict mode, unmapped findings are "
                "classified as false positives."
            ),

            "duplicate_note": (
                "Duplicate matches are reported separately "
                "and are not counted as additional true "
                "positives or false positives."
            ),

            "ambiguous_note": (
                "Ambiguous matches are reported separately "
                "and are not included in precision, recall "
                "or F1 calculations."
            ),
        },
    }

    write_json(
        output_path,
        output_document,
    )

    print("Generic metrics calculation completed.")
    print(f"Case: {case_id}")
    print(f"Scanner: {scanner}")
    print(f"Matching mode: {matching_mode}")
    print(
        f"True positives: "
        f"{true_positive_count}"
    )
    print(
        f"False positives: "
        f"{false_positive_count}"
    )
    print(
        f"False negatives: "
        f"{false_negative_count}"
    )
    print(
        f"Unlabelled extras: "
        f"{unlabelled_extra_count}"
    )
    print(
        f"Duplicate matches: "
        f"{duplicate_match_count}"
    )
    print(
        f"Ambiguous matches: "
        f"{ambiguous_match_count}"
    )
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 score: {f1_score}")
    print(
        f"Evaluation status: "
        f"{evaluation_status}"
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
        MetricsError,
    ) as error:
        print()
        print("Generic metrics calculation failed.")
        print(f"Reason: {error}")
        return 1

    except KeyboardInterrupt:
        print()
        print("Metrics calculation cancelled.")
        return 130

    except Exception as error:
        print()
        print("Unexpected metrics calculation error.")
        print(
            f"{type(error).__name__}: {error}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
