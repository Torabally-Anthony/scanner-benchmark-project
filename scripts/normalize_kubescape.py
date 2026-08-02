from pathlib import Path
import json


CASE_ID = "case-001-privileged-container"
TOOL_NAME = "kubescape"
ARTIFACT_TYPE = "kubernetes_yaml"

RAW_FILE = Path("results/raw/kubescape/case-001-privileged-container.json")
VERSION_FILE = Path("results/raw/kubescape/kubescape-version.txt")
OUTPUT_FILE = Path("results/normalised/kubescape/case-001-privileged-container.normalised.json")


RULE_MAPPING = {
    "C-0057": {
        "category": "PodSecurity",
        "subcategory": "PrivilegedContainer",
        "severity": "High",
        "expected_field_path": "spec.template.spec.containers[0].securityContext.privileged",
        "expected_bad_value": True,
        "expected_secure_value": False,
        "ground_truth_id": "GT-001",
        "resource": "Deployment.default.privileged-demo-app",
        "container": "demo-container",
    }
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def load_version(path: Path) -> str:
    if not path.exists():
        return "unknown"

    text = path.read_text(encoding="utf-8-sig").strip()

    if not text:
        return "unknown"

    return text


def get_control_category(control: dict) -> tuple[str | None, str | None]:
    category = control.get("category") or {}

    category_name = category.get("name")

    subcategory = category.get("subCategory") or {}
    subcategory_name = subcategory.get("name")

    return category_name, subcategory_name


def normalise_control(control_id: str, control: dict, scanner_version: str) -> dict:
    mapping = RULE_MAPPING.get(control_id)

    original_category, original_subcategory = get_control_category(control)

    if mapping:
        mapping_status = "mapped"
        category = mapping["category"]
        subcategory = mapping["subcategory"]
        severity = mapping["severity"]
        expected_field_path = mapping["expected_field_path"]
        ground_truth_id = mapping["ground_truth_id"]
        resource = mapping["resource"]
        container = mapping["container"]
    else:
        mapping_status = "unmapped"
        category = original_category
        subcategory = original_subcategory
        severity = control.get("severity")
        expected_field_path = None
        ground_truth_id = None
        resource = "Unknown"
        container = "Unknown"

    resource_counters = control.get("ResourceCounters") or {}
    status_info = control.get("statusInfo") or {}

    return {
        "case_id": CASE_ID,
        "tool": TOOL_NAME,
        "scanner_version": scanner_version,
        "artifact_type": ARTIFACT_TYPE,
        "target": "artifact.yaml",

        "rule_id": control_id,
        "rule_name": control.get("name"),
        "severity": severity,
        "status": control.get("status"),

        "category": category,
        "subcategory": subcategory,
        "original_category": original_category,
        "original_subcategory": original_subcategory,

        "mapping_status": mapping_status,
        "ground_truth_id": ground_truth_id,

        "resource": resource,
        "container": container,
        "expected_field_path": expected_field_path,

        "message": f"Kubescape control {control_id} failed: {control.get('name')}",
        "status_info": status_info,
        "failed_resources": resource_counters.get("failedResources", 0),
        "passed_resources": resource_counters.get("passedResources", 0),
        "skipped_resources": resource_counters.get("skippedResources", 0),
        "score": control.get("score"),
        "compliance_score": control.get("complianceScore"),
    }


def main() -> None:
    raw_data = load_json(RAW_FILE)
    scanner_version = load_version(VERSION_FILE)

    controls = raw_data.get("summaryDetails", {}).get("controls", {})

    if not controls:
        raise KeyError("Could not find summaryDetails.controls in Kubescape JSON.")

    normalised_findings = []

    for control_id, control in controls.items():
        status = control.get("status")

        # For this benchmark, we normalise failed controls only.
        if status != "failed":
            continue

        normalised_findings.append(
            normalise_control(
                control_id=control_id,
                control=control,
                scanner_version=scanner_version,
            )
        )

    mapped_count = sum(
        1 for finding in normalised_findings
        if finding["mapping_status"] == "mapped"
    )

    unmapped_count = sum(
        1 for finding in normalised_findings
        if finding["mapping_status"] == "unmapped"
    )

    output = {
        "case_id": CASE_ID,
        "tool": TOOL_NAME,
        "scanner_version": scanner_version,
        "artifact_type": ARTIFACT_TYPE,
        "source_file": str(RAW_FILE),

        "summary": {
            "total_controls_count": len(controls),
            "normalised_findings_count": len(normalised_findings),
            "mapped_findings_count": mapped_count,
            "unmapped_findings_count": unmapped_count,
        },

        "normalised_findings": normalised_findings,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print("Kubescape normalisation completed.")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total controls: {len(controls)}")
    print(f"Normalised failed findings: {len(normalised_findings)}")
    print(f"Mapped findings: {mapped_count}")
    print(f"Unmapped findings: {unmapped_count}")


if __name__ == "__main__":
    main()