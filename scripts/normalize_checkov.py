from pathlib import Path
import json


RAW_FILE = Path("results/raw/checkov/case-001-privileged-container.json")
OUTPUT_DIR = Path("results/normalised/checkov")
OUTPUT_FILE = OUTPUT_DIR / "case-001-privileged-container.normalised.json"

CASE_ID = "case-001-privileged-container"
ARTIFACT_TYPE = "kubernetes_yaml"
TOOL_NAME = "checkov"


# This is our first simple rule-mapping table.
# Later, we will expand this when we add more benchmark cases.
RULE_MAPPING = {
    "CKV_K8S_16": {
        "category": "PodSecurity",
        "subcategory": "PrivilegedContainer",
        "severity": "High",
        "expected_field_path": "spec.template.spec.containers[0].securityContext.privileged",
    }
}


def load_json(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"Raw Checkov file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def get_rule_mapping(check_id: str) -> dict:
    """
    Returns our project category mapping for a Checkov rule.
    If we do not know the rule yet, we mark it as Unmapped.
    """
    return RULE_MAPPING.get(
        check_id,
        {
            "category": "Unmapped",
            "subcategory": "Unmapped",
            "severity": "Unknown",
            "expected_field_path": None,
        },
    )


def normalise_failed_check(finding: dict) -> dict:
    check_id = finding.get("check_id")
    mapping = get_rule_mapping(check_id)

    return {
        "tool": TOOL_NAME,
        "case_id": CASE_ID,
        "artifact_type": ARTIFACT_TYPE,

        "rule_id": check_id,
        "rule_name": finding.get("check_name"),
        "result": finding.get("check_result", {}).get("result"),

        "category": mapping["category"],
        "subcategory": mapping["subcategory"],
        "severity": mapping["severity"],

        "resource": finding.get("resource"),
        "file_path": finding.get("repo_file_path") or finding.get("file_path"),
        "line_range": finding.get("file_line_range"),

        "expected_field_path": mapping["expected_field_path"],
        "message": finding.get("check_name"),

        # This tells us whether this rule is part of our current mapping table.
        # For this first case, CKV_K8S_16 should be mapped.
        "mapping_status": "mapped" if check_id in RULE_MAPPING else "unmapped",
    }


def main():
    print("Normalising Checkov output...")

    raw_data = load_json(RAW_FILE)

    results = raw_data.get("results", {})
    failed_checks = results.get("failed_checks", [])
    passed_checks = results.get("passed_checks", [])

    normalised_findings = []

    for failed_check in failed_checks:
        normalised_findings.append(normalise_failed_check(failed_check))

    output = {
        "case_id": CASE_ID,
        "tool": TOOL_NAME,
        "artifact_type": ARTIFACT_TYPE,
        "source_file": str(RAW_FILE),

        "summary": {
            "failed_checks_count": len(failed_checks),
            "passed_checks_count": len(passed_checks),
            "normalised_findings_count": len(normalised_findings),
            "mapped_findings_count": len(
                [
                    finding
                    for finding in normalised_findings
                    if finding["mapping_status"] == "mapped"
                ]
            ),
            "unmapped_findings_count": len(
                [
                    finding
                    for finding in normalised_findings
                    if finding["mapping_status"] == "unmapped"
                ]
            ),
        },

        "findings": normalised_findings,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print(f"Normalised output saved to: {OUTPUT_FILE}")
    print(f"Failed checks normalised: {len(normalised_findings)}")

    mapped = output["summary"]["mapped_findings_count"]
    unmapped = output["summary"]["unmapped_findings_count"]

    print(f"Mapped findings: {mapped}")
    print(f"Unmapped findings: {unmapped}")

    if mapped > 0:
        print("Checkov detected at least one finding mapped to our ground truth.")
    else:
        print("No mapped ground-truth finding detected yet.")


if __name__ == "__main__":
    main()