from pathlib import Path
import json
import yaml


CASE_ID = "case-001-privileged-container"
TOOL_NAME = "trivy"

NORMALISED_FILE = Path("results/normalised/trivy/case-001-privileged-container.normalised.json")
GROUND_TRUTH_FILE = Path("corpus/kubernetes/case-001-privileged-container/ground_truth.yaml")
OUTPUT_FILE = Path("results/matched/trivy/case-001-privileged-container.matched.json")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("r", encoding="utf-8-sig") as file:
        return yaml.safe_load(file)


def extract_ground_truth_items(ground_truth_data: dict) -> list[dict]:
    """
    Supports the ground_truth.yaml structure used in this project.
    """

    if "misconfigurations" in ground_truth_data:
        return ground_truth_data["misconfigurations"]

    if "ground_truth" in ground_truth_data:
        return ground_truth_data["ground_truth"]

    if "items" in ground_truth_data:
        return ground_truth_data["items"]

    raise KeyError("Could not find ground truth items in ground_truth.yaml")


def finding_matches_ground_truth(finding: dict, ground_truth: dict) -> bool:
    same_ground_truth_id = finding.get("ground_truth_id") == ground_truth.get("id")

    same_category = finding.get("category") == ground_truth.get("category")
    same_subcategory = finding.get("subcategory") == ground_truth.get("subcategory")

    same_field_path = (
        finding.get("expected_field_path") == ground_truth.get("field_path")
    )

    return same_ground_truth_id and same_category and same_subcategory and same_field_path


def main() -> None:
    normalised_data = load_json(NORMALISED_FILE)
    ground_truth_data = load_yaml(GROUND_TRUTH_FILE)

    findings = normalised_data.get("normalised_findings", [])
    ground_truth_items = extract_ground_truth_items(ground_truth_data)

    true_positives = []
    false_negatives = []
    unlabelled_extra_findings = []

    matched_ground_truth_ids = set()

    mapped_findings = [
        finding for finding in findings
        if finding.get("mapping_status") == "mapped"
    ]

    unmapped_findings = [
        finding for finding in findings
        if finding.get("mapping_status") == "unmapped"
    ]

    for ground_truth in ground_truth_items:
        matched_finding = None

        for finding in mapped_findings:
            if finding_matches_ground_truth(finding, ground_truth):
                matched_finding = finding
                break

        if matched_finding:
            matched_ground_truth_ids.add(ground_truth.get("id"))

            true_positives.append({
                "match_status": "TRUE_POSITIVE",
                "ground_truth_id": ground_truth.get("id"),
                "scanner_rule_id": matched_finding.get("rule_id"),
                "scanner_rule_name": matched_finding.get("rule_name"),
                "resource": matched_finding.get("resource"),
                "container": matched_finding.get("container"),
                "field_path": matched_finding.get("expected_field_path"),
                "evidence_message": matched_finding.get("message"),
            })
        else:
            false_negatives.append({
                "match_status": "FALSE_NEGATIVE",
                "ground_truth_id": ground_truth.get("id"),
                "category": ground_truth.get("category"),
                "subcategory": ground_truth.get("subcategory"),
                "field_path": ground_truth.get("field_path"),
                "missed_reason": "No mapped Trivy finding matched this ground truth item.",
            })

    for finding in unmapped_findings:
        unlabelled_extra_findings.append({
            "match_status": "UNLABELLED_EXTRA",
            "scanner_rule_id": finding.get("rule_id"),
            "scanner_rule_name": finding.get("rule_name"),
            "severity": finding.get("severity"),
            "resource": finding.get("resource"),
            "container": finding.get("container"),
            "message": finding.get("message"),
        })

    output = {
        "case_id": CASE_ID,
        "tool": TOOL_NAME,
        "source_file": str(NORMALISED_FILE),

        "summary": {
            "ground_truth_items_count": len(ground_truth_items),
            "normalised_findings_count": len(findings),
            "mapped_findings_count": len(mapped_findings),
            "unmapped_findings_count": len(unmapped_findings),

            "true_positive_count": len(true_positives),
            "false_negative_count": len(false_negatives),

            "unlabelled_extra_findings_count": len(unlabelled_extra_findings),

            # Review mode: unmapped findings are not counted as false positives yet.
            "false_positive_count": 0,
        },

        "true_positives": true_positives,
        "false_negatives": false_negatives,
        "unlabelled_extra_findings": unlabelled_extra_findings,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print("Trivy matching completed.")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"True positives: {len(true_positives)}")
    print(f"False negatives: {len(false_negatives)}")
    print(f"Unlabelled extra findings: {len(unlabelled_extra_findings)}")
    print("False positives: 0")
    print("Review mode: unmapped findings are stored as unlabelled extras.")


if __name__ == "__main__":
    main()