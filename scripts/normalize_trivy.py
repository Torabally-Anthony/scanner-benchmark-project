from pathlib import Path
import json
import re


CASE_ID = "case-001-privileged-container"
TOOL_NAME = "trivy"
ARTIFACT_TYPE = "kubernetes_yaml"

RAW_FILE = Path("results/raw/trivy/case-001-privileged-container.json")
OUTPUT_FILE = Path("results/normalised/trivy/case-001-privileged-container.normalised.json")


RULE_MAPPING = {
    "KSV-0017": {
        "category": "PodSecurity",
        "subcategory": "PrivilegedContainer",
        "severity": "High",
        "expected_field_path": "spec.template.spec.containers[0].securityContext.privileged",
        "expected_bad_value": True,
        "expected_secure_value": False,
        "ground_truth_id": "GT-001",
    }
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def extract_resource_and_container(message: str) -> tuple[str, str]:
    """
    Tries to extract Deployment and container names from Trivy's message.
    Example:
    Container 'demo-container' of Deployment 'privileged-demo-app'
    """

    container_name = None
    deployment_name = None

    container_match = re.search(
        r"[Cc]ontainer ['\"]([^'\"]+)['\"]",
        message or "",
    )

    deployment_match = re.search(
        r"[Dd]eployment ['\"]([^'\"]+)['\"]",
        message or "",
    )

    if container_match:
        container_name = container_match.group(1)

    if deployment_match:
        deployment_name = deployment_match.group(1)

    if deployment_name:
        resource = f"Deployment.default.{deployment_name}"
    else:
        resource = "Unknown"

    return resource, container_name or "Unknown"


def normalise_misconfiguration(misconfiguration: dict, target: str, scanner_version: str) -> dict:
    rule_id = misconfiguration.get("ID")
    mapping = RULE_MAPPING.get(rule_id)

    message = misconfiguration.get("Message", "")
    resource, container_name = extract_resource_and_container(message)

    cause_metadata = misconfiguration.get("CauseMetadata") or {}

    if mapping:
        mapping_status = "mapped"
        category = mapping["category"]
        subcategory = mapping["subcategory"]
        severity = mapping["severity"]
        expected_field_path = mapping["expected_field_path"]
        ground_truth_id = mapping["ground_truth_id"]
    else:
        mapping_status = "unmapped"
        category = None
        subcategory = None
        severity = str(misconfiguration.get("Severity", "")).title()
        expected_field_path = None
        ground_truth_id = None

    return {
        "case_id": CASE_ID,
        "tool": TOOL_NAME,
        "scanner_version": scanner_version,
        "artifact_type": ARTIFACT_TYPE,
        "target": target,

        "rule_id": rule_id,
        "rule_name": misconfiguration.get("Title"),
        "description": misconfiguration.get("Description"),
        "severity": severity,
        "status": misconfiguration.get("Status"),

        "category": category,
        "subcategory": subcategory,
        "mapping_status": mapping_status,
        "ground_truth_id": ground_truth_id,

        "resource": resource,
        "container": container_name,
        "expected_field_path": expected_field_path,

        "message": message,
        "resolution": misconfiguration.get("Resolution"),
        "primary_url": misconfiguration.get("PrimaryURL"),

        "start_line": cause_metadata.get("StartLine"),
        "end_line": cause_metadata.get("EndLine"),
    }


def main() -> None:
    raw_data = load_json(RAW_FILE)

    scanner_version = raw_data.get("Trivy", {}).get("Version", "unknown")
    results = raw_data.get("Results", [])

    normalised_findings = []

    for result in results:
        target = result.get("Target")
        misconfigurations = result.get("Misconfigurations") or []

        for misconfiguration in misconfigurations:
            normalised = normalise_misconfiguration(
                misconfiguration=misconfiguration,
                target=target,
                scanner_version=scanner_version,
            )
            normalised_findings.append(normalised)

    mapped_count = sum(1 for finding in normalised_findings if finding["mapping_status"] == "mapped")
    unmapped_count = sum(1 for finding in normalised_findings if finding["mapping_status"] == "unmapped")

    output = {
        "case_id": CASE_ID,
        "tool": TOOL_NAME,
        "scanner_version": scanner_version,
        "artifact_type": ARTIFACT_TYPE,
        "source_file": str(RAW_FILE),

        "summary": {
            "normalised_findings_count": len(normalised_findings),
            "mapped_findings_count": mapped_count,
            "unmapped_findings_count": unmapped_count,
        },

        "normalised_findings": normalised_findings,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print("Trivy normalisation completed.")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Normalised findings: {len(normalised_findings)}")
    print(f"Mapped findings: {mapped_count}")
    print(f"Unmapped findings: {unmapped_count}")


if __name__ == "__main__":
    main()