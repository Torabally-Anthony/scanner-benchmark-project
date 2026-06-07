from pathlib import Path
import json
import yaml


NORMALISED_FILE = Path(
    "results/normalised/checkov/case-001-privileged-container.normalised.json"
)

GROUND_TRUTH_FILE = Path(
    "corpus/kubernetes/case-001-privileged-container/ground_truth.yaml"
)

OUTPUT_DIR = Path("results/matched/checkov")
OUTPUT_FILE = OUTPUT_DIR / "case-001-privileged-container.matched.json"


def load_json(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing JSON file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_yaml(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing YAML file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def finding_matches_ground_truth(finding: dict, ground_truth_item: dict) -> bool:
    """
    A finding matches ground truth when the important benchmark fields match.

    For this first project version, we match using:
    - category
    - subcategory
    - expected field path
    """

    same_category = finding.get("category") == ground_truth_item.get("category")
    same_subcategory = finding.get("subcategory") == ground_truth_item.get("subcategory")
    same_field_path = finding.get("expected_field_path") == ground_truth_item.get("field_path")

    return same_category and same_subcategory and same_field_path


def main():
    print("Matching Checkov findings to ground truth...")

    normalised_data = load_json(NORMALISED_FILE)
    ground_truth_data = load_yaml(GROUND_TRUTH_FILE)

    findings = normalised_data.get("findings", [])
    ground_truth_items = ground_truth_data.get("misconfigurations", [])

    true_positives = []
    false_negatives = []
    unlabelled_extra_findings = []

    matched_ground_truth_ids = set()

    # Step 1: Try to match each normalised scanner finding to ground truth
    for finding in findings:
        matched = False

        for ground_truth_item in ground_truth_items:
            if finding_matches_ground_truth(finding, ground_truth_item):
                true_positives.append(
                    {
                        "ground_truth_id": ground_truth_item.get("id"),
                        "scanner_rule_id": finding.get("rule_id"),
                        "scanner_rule_name": finding.get("rule_name"),
                        "category": finding.get("category"),
                        "subcategory": finding.get("subcategory"),
                        "resource": finding.get("resource"),
                        "field_path": ground_truth_item.get("field_path"),
                        "match_status": "true_positive",
                    }
                )

                matched_ground_truth_ids.add(ground_truth_item.get("id"))
                matched = True
                break

        # In review mode, we do not immediately count unmapped findings as false positives.
        # We store them separately as unlabelled extra findings.
        if not matched and finding.get("mapping_status") == "unmapped":
            unlabelled_extra_findings.append(
                {
                    "scanner_rule_id": finding.get("rule_id"),
                    "scanner_rule_name": finding.get("rule_name"),
                    "resource": finding.get("resource"),
                    "category": finding.get("category"),
                    "subcategory": finding.get("subcategory"),
                    "match_status": "unlabelled_extra_finding",
                }
            )

    # Step 2: Check if any ground-truth item was missed
    for ground_truth_item in ground_truth_items:
        ground_truth_id = ground_truth_item.get("id")

        if ground_truth_id not in matched_ground_truth_ids:
            false_negatives.append(
                {
                    "ground_truth_id": ground_truth_id,
                    "category": ground_truth_item.get("category"),
                    "subcategory": ground_truth_item.get("subcategory"),
                    "resource": ground_truth_item.get("resource"),
                    "field_path": ground_truth_item.get("field_path"),
                    "match_status": "false_negative",
                }
            )

    output = {
        "case_id": normalised_data.get("case_id"),
        "tool": normalised_data.get("tool"),
        "artifact_type": normalised_data.get("artifact_type"),
        "matching_mode": "review_mode",

        "summary": {
            "ground_truth_items_count": len(ground_truth_items),
            "normalised_findings_count": len(findings),
            "true_positive_count": len(true_positives),
            "false_negative_count": len(false_negatives),

            # In review mode, these are not counted as false positives yet.
            "unlabelled_extra_findings_count": len(unlabelled_extra_findings),

            # For now, false positives are 0 because we are not using strict mode yet.
            "false_positive_count": 0,
        },

        "true_positives": true_positives,
        "false_negatives": false_negatives,
        "unlabelled_extra_findings": unlabelled_extra_findings,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print(f"Matched output saved to: {OUTPUT_FILE}")
    print(f"True positives: {len(true_positives)}")
    print(f"False negatives: {len(false_negatives)}")
    print(f"Unlabelled extra findings: {len(unlabelled_extra_findings)}")
    print("Matching completed.")


if __name__ == "__main__":
    main()