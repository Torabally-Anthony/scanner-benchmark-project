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


class MatchingError(Exception):
    """Raised when normalised findings cannot be matched."""


# This function reads a JSON file and confirms that its root is an object.
def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file and confirm that its root is an object."""

    if not path.exists():
        raise MatchingError(
            f"Normalised findings file does not exist: {path}"
        )

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise MatchingError(
            f"Invalid JSON in {path.name}: {error}"
        ) from error

    except OSError as error:
        raise MatchingError(
            f"Could not read {path}: {error}"
        ) from error

    if not isinstance(data, dict):
        raise MatchingError(
            f"The root of {path.name} must be a JSON object."
        )

    return data


# This function writes formatted JSON to disk.
def write_json(
    path: Path,
    content: dict[str, Any],
) -> None:
    """Write formatted JSON to disk."""

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
        raise MatchingError(
            f"Could not write output file: {error}"
        ) from error


# This function validates the normalised file and returns its findings.
def validate_normalised_document(
    document: dict[str, Any],
    expected_case_id: str,
    expected_scanner: str,
) -> list[dict[str, Any]]:
    """Validate the normalised file and return its findings."""

    document_case_id = document.get("case_id")
    document_scanner = document.get("tool")

    if document_case_id != expected_case_id:
        raise MatchingError(
            "The normalised file case ID does not match "
            f"the requested case. Expected '{expected_case_id}', "
            f"found '{document_case_id}'."
        )

    if document_scanner != expected_scanner:
        raise MatchingError(
            "The normalised file scanner does not match "
            f"the requested scanner. Expected '{expected_scanner}', "
            f"found '{document_scanner}'."
        )

    findings = document.get("findings")

    if not isinstance(findings, list):
        raise MatchingError(
            "The normalised file must contain a 'findings' list."
        )

    valid_findings: list[dict[str, Any]] = []

    for index, finding in enumerate(
        findings,
        start=1,
    ):
        if not isinstance(finding, dict):
            raise MatchingError(
                f"Normalised finding {index} is not a JSON object."
            )

        valid_findings.append(finding)

    return valid_findings


# This function returns a stripped string or None.
def clean_text(value: Any) -> str | None:
    """Return a stripped string or None."""

    if not isinstance(value, str):
        return None

    cleaned_value = value.strip()

    return cleaned_value or None


# This function copies a finding and adds matching information.
def create_classified_finding(
    finding: dict[str, Any],
    classification: str,
    reason: str,
) -> dict[str, Any]:
    """Copy a finding and add matching information."""

    classified_finding = dict(finding)

    classified_finding["classification"] = classification
    classified_finding["classification_reason"] = reason

    return classified_finding


# This function creates a false-negative record from ground truth.
def create_false_negative(
    ground_truth_id: str,
    ground_truth_item: dict[str, Any],
) -> dict[str, Any]:
    """Create a false-negative record from ground truth."""

    return {
        "classification": "false_negative",
        "classification_reason": (
            "No scanner finding matched this "
            "ground-truth issue."
        ),
        "ground_truth_id": ground_truth_id,
        "category": ground_truth_item.get("category"),
        "subcategory": ground_truth_item.get(
            "subcategory"
        ),
        "severity": ground_truth_item.get("severity"),
        "resource": ground_truth_item.get("resource"),
        "container": ground_truth_item.get("container"),
        "field_path": ground_truth_item.get(
            "field_path"
        ),
        "bad_value": ground_truth_item.get("bad_value"),
        "expected_secure_value": (
            ground_truth_item.get(
                "expected_secure_value"
            )
        ),
        "ground_truth": ground_truth_item,
    }


# This function classifies normalised findings.
def match_findings_to_ground_truth(
    findings: list[dict[str, Any]],
    ground_truth_items: dict[str, dict[str, Any]],
    matching_mode: str,
) -> dict[str, list[dict[str, Any]]]:
    """
    Classify normalised findings.

    Review mode:
        mapped finding   -> true positive or duplicate
        unmapped finding -> unlabelled extra

    Strict mode:
        mapped finding   -> true positive or duplicate
        unmapped finding -> false positive

    Any undetected ground-truth item becomes a false negative.
    """

    true_positives: list[dict[str, Any]] = []
    false_positives: list[dict[str, Any]] = []
    unlabelled_extras: list[dict[str, Any]] = []
    duplicate_matches: list[dict[str, Any]] = []
    ambiguous_matches: list[dict[str, Any]] = []

    matched_ground_truth_ids: set[str] = set()

    for finding in findings:
        mapping_status = clean_text(
            finding.get("mapping_status")
        )

        if mapping_status is not None:
            mapping_status = mapping_status.lower()

        ground_truth_id = clean_text(
            finding.get("ground_truth_id")
        )

        # A finding says it is mapped.
        if mapping_status == "mapped":

            # It cannot be confidently matched without an ID.
            if ground_truth_id is None:
                ambiguous_matches.append(
                    create_classified_finding(
                        finding=finding,
                        classification="ambiguous_match",
                        reason=(
                            "The finding is marked as mapped, "
                            "but it has no ground_truth_id."
                        ),
                    )
                )

                continue

            # The ID exists in the finding but not in ground truth.
            if ground_truth_id not in ground_truth_items:
                ambiguous_matches.append(
                    create_classified_finding(
                        finding=finding,
                        classification="ambiguous_match",
                        reason=(
                            f"The finding refers to "
                            f"'{ground_truth_id}', but that ID "
                            "does not exist in ground_truth.yaml."
                        ),
                    )
                )

                continue

            # Only the first detection counts as a TP so repeated alerts cannot inflate the score.
            if ground_truth_id in matched_ground_truth_ids:
                duplicate_matches.append(
                    create_classified_finding(
                        finding=finding,
                        classification="duplicate_match",
                        reason=(
                            f"Ground-truth issue "
                            f"'{ground_truth_id}' was already "
                            "matched by another finding."
                        ),
                    )
                )

                continue

            # This is the first valid detection of the issue.
            matched_ground_truth_ids.add(
                ground_truth_id
            )

            true_positives.append(
                create_classified_finding(
                    finding=finding,
                    classification="true_positive",
                    reason=(
                        f"The scanner rule correctly matched "
                        f"ground-truth issue "
                        f"'{ground_truth_id}'."
                    ),
                )
            )

            continue

        # A finding says it is unmapped.
        if mapping_status == "unmapped":

            # An unmapped finding should not already contain
            # a ground-truth ID.
            if ground_truth_id is not None:
                ambiguous_matches.append(
                    create_classified_finding(
                        finding=finding,
                        classification="ambiguous_match",
                        reason=(
                            "The finding is marked as unmapped, "
                            "but it contains a ground_truth_id."
                        ),
                    )
                )

                continue

            # Review preserves unverified extras; strict mode assumes every extra is an FP.
            if matching_mode == "review":
                unlabelled_extras.append(
                    create_classified_finding(
                        finding=finding,
                        classification="unlabelled_extra",
                        reason=(
                            "The finding has no approved "
                            "ground-truth mapping. In review mode, "
                            "it is stored as an unlabelled extra "
                            "rather than a false positive."
                        ),
                    )
                )

            else:
                false_positives.append(
                    create_classified_finding(
                        finding=finding,
                        classification="false_positive",
                        reason=(
                            "The finding has no ground-truth "
                            "mapping and strict mode treats all "
                            "unmapped findings as false positives."
                        ),
                    )
                )

            continue

        # Any other or missing mapping status is uncertain.
        ambiguous_matches.append(
            create_classified_finding(
                finding=finding,
                classification="ambiguous_match",
                reason=(
                    "The finding has an unknown or missing "
                    f"mapping_status: {mapping_status!r}."
                ),
            )
        )

    false_negatives: list[dict[str, Any]] = []

    # Any expected issue left unmatched is a detection the scanner missed.
    for ground_truth_id, ground_truth_item in (
        ground_truth_items.items()
    ):
        if ground_truth_id in matched_ground_truth_ids:
            continue

        false_negatives.append(
            create_false_negative(
                ground_truth_id=ground_truth_id,
                ground_truth_item=ground_truth_item,
            )
        )

    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "unlabelled_extras": unlabelled_extras,
        "duplicate_matches": duplicate_matches,
        "ambiguous_matches": ambiguous_matches,
    }


# This function reads command-line arguments.
def parse_arguments() -> argparse.Namespace:
    """Read command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Match generic normalised scanner findings "
            "against benchmark ground truth."
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
        help="Scanner whose findings will be matched.",
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
        "--input-root",
        default="results/normalised_generic",
        help=(
            "Directory containing the generic "
            "normalised findings."
        ),
    )

    parser.add_argument(
        "--output-root",
        default="results/matched_generic",
        help=(
            "Output directory. The default avoids "
            "overwriting existing matched results."
        ),
    )

    return parser.parse_args()


# This function resolves and validates a project-relative directory.
def resolve_internal_directory(
    directory_value: str,
    field_name: str,
) -> Path:
    """Resolve and validate a project-relative directory."""

    directory = (
        PROJECT_ROOT / directory_value
    ).resolve()

    # Reject path traversal so input and output cannot escape the project directory.
    try:
        directory.relative_to(PROJECT_ROOT)

    except ValueError as error:
        raise MatchingError(
            f"{field_name} must be inside the project directory."
        ) from error

    return directory


# This function runs the generic ground-truth matching process.
def run() -> Path:
    """Run the generic ground-truth matching process."""

    arguments = parse_arguments()

    case_id = arguments.case_id.strip()
    scanner = arguments.scanner.strip().lower()

    configuration = load_benchmark_config()

    case_configuration = get_case_configuration(
        configuration,
        case_id,
    )

    defaults = configuration.get(
        "defaults",
        {},
    )

    if not isinstance(defaults, dict):
        defaults = {}

    matching_mode = (
        arguments.matching_mode
        or defaults.get("matching_mode")
        or "review"
    )

    matching_mode = str(
        matching_mode
    ).strip().lower()

    if matching_mode not in SUPPORTED_MATCHING_MODES:
        raise MatchingError(
            "Matching mode must be 'review' or 'strict'."
        )

    ground_truth = load_case_ground_truth(
        case_configuration
    )

    ground_truth_items = get_ground_truth_items(
        ground_truth
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
        / f"{case_id}.normalised.json"
    )

    normalised_document = read_json(
        input_path
    )

    findings = validate_normalised_document(
        document=normalised_document,
        expected_case_id=case_id,
        expected_scanner=scanner,
    )

    classifications = (
        match_findings_to_ground_truth(
            findings=findings,
            ground_truth_items=ground_truth_items,
            matching_mode=matching_mode,
        )
    )

    true_positives = classifications[
        "true_positives"
    ]

    false_positives = classifications[
        "false_positives"
    ]

    false_negatives = classifications[
        "false_negatives"
    ]

    unlabelled_extras = classifications[
        "unlabelled_extras"
    ]

    duplicate_matches = classifications[
        "duplicate_matches"
    ]

    ambiguous_matches = classifications[
        "ambiguous_matches"
    ]

    matched_ground_truth_ids = sorted(
        {
            finding["ground_truth_id"]
            for finding in true_positives
            if finding.get("ground_truth_id")
        }
    )

    unmatched_ground_truth_ids = sorted(
        {
            finding["ground_truth_id"]
            for finding in false_negatives
            if finding.get("ground_truth_id")
        }
    )

    output_path = (
        output_root
        / scanner
        / f"{case_id}.matched.json"
    )

    ground_truth_source = case_configuration.get(
        "ground_truth_path"
    )

    output_document = {
        "schema_version": "1.0",
        "case_id": case_id,
        "tool": scanner,
        "scanner_version": normalised_document.get(
            "scanner_version"
        ),
        "artifact_type": normalised_document.get(
            "artifact_type"
        ),
        "matching_mode": matching_mode,
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "source_file": str(
            input_path.relative_to(PROJECT_ROOT)
        ),

        "ground_truth_source": ground_truth_source,

        "classification_policy": {
            "true_positive": (
                "The first valid scanner finding mapped "
                "to a ground-truth issue."
            ),
            "false_negative": (
                "A ground-truth issue with no valid "
                "scanner detection."
            ),
            "unlabelled_extra": (
                "An unmapped finding retained for review."
            ),
            "false_positive": (
                "An unmapped finding classified as "
                "incorrect in strict mode."
            ),
            "duplicate_match": (
                "An additional finding mapped to a "
                "ground-truth issue already detected."
            ),
            "ambiguous_match": (
                "A finding with inconsistent or incomplete "
                "mapping information."
            ),
        },

        "counts": {
            "total_normalised_findings": len(
                findings
            ),
            "ground_truth_issue_count": len(
                ground_truth_items
            ),
            "true_positive_count": len(
                true_positives
            ),
            "false_positive_count": len(
                false_positives
            ),
            "false_negative_count": len(
                false_negatives
            ),
            "unlabelled_extra_findings_count": len(
                unlabelled_extras
            ),
            "duplicate_match_count": len(
                duplicate_matches
            ),
            "ambiguous_match_count": len(
                ambiguous_matches
            ),
        },

        "matched_ground_truth_ids": (
            matched_ground_truth_ids
        ),

        "unmatched_ground_truth_ids": (
            unmatched_ground_truth_ids
        ),

        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "unlabelled_extras": unlabelled_extras,
        "duplicate_matches": duplicate_matches,
        "ambiguous_matches": ambiguous_matches,
    }

    write_json(
        output_path,
        output_document,
    )

    print("Generic ground-truth matching completed.")
    print(f"Case: {case_id}")
    print(f"Scanner: {scanner}")
    print(f"Matching mode: {matching_mode}")
    print(f"Normalised findings: {len(findings)}")
    print(
        f"Ground-truth issues: "
        f"{len(ground_truth_items)}"
    )
    print(
        f"True positives: "
        f"{len(true_positives)}"
    )
    print(
        f"False positives: "
        f"{len(false_positives)}"
    )
    print(
        f"False negatives: "
        f"{len(false_negatives)}"
    )
    print(
        f"Unlabelled extras: "
        f"{len(unlabelled_extras)}"
    )
    print(
        f"Duplicate matches: "
        f"{len(duplicate_matches)}"
    )
    print(
        f"Ambiguous matches: "
        f"{len(ambiguous_matches)}"
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
        MatchingError,
    ) as error:
        print()
        print("Generic ground-truth matching failed.")
        print(f"Reason: {error}")
        return 1

    except KeyboardInterrupt:
        print()
        print("Ground-truth matching cancelled.")
        return 130

    except Exception as error:
        print()
        print("Unexpected ground-truth matching error.")
        print(
            f"{type(error).__name__}: {error}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
