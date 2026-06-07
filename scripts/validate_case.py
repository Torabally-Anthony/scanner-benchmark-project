from pathlib import Path
import yaml

CASE_PATH = Path("corpus/kubernetes/case-001-privileged-container")

artifact_file = CASE_PATH / "artifact.yaml"
ground_truth_file = CASE_PATH / "ground_truth.yaml"

def load_yaml(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def main():
    print("Validating case-001-privileged-container...")

    artifact = load_yaml(artifact_file)
    ground_truth = load_yaml(ground_truth_file)

    print("artifact.yaml loaded successfully.")
    print("ground_truth.yaml loaded successfully.")

    container = artifact["spec"]["template"]["spec"]["containers"][0]
    privileged_value = container.get("securityContext", {}).get("privileged")

    if privileged_value is True:
        print("Privileged container misconfiguration found in artifact.yaml.")
    else:
        raise ValueError("Expected privileged: true but did not find it.")

    case_id = ground_truth.get("case_id")
    misconfigs = ground_truth.get("misconfigurations", [])

    if case_id != "case-001-privileged-container":
        raise ValueError("case_id does not match expected case ID.")

    if not misconfigs:
        raise ValueError("No misconfigurations found in ground_truth.yaml.")

    first_misconfig = misconfigs[0]

    expected_field = "spec.template.spec.containers[0].securityContext.privileged"

    if first_misconfig.get("field_path") != expected_field:
        raise ValueError("field_path in ground_truth.yaml does not match expected path.")

    if first_misconfig.get("bad_value") is not True:
        raise ValueError("bad_value in ground_truth.yaml should be true.")

    print("ground_truth.yaml correctly describes the privileged container issue.")
    print("Case validation passed.")

if __name__ == "__main__":
    main()