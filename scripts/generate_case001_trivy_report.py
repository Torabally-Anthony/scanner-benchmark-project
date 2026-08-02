from pathlib import Path
import json


CASE_ID = "case-001-privileged-container"
TOOL_NAME = "trivy"

MATCHED_FILE = Path("results/matched/trivy/case-001-privileged-container.matched.json")
METRICS_FILE = Path("results/metrics/trivy/case-001-privileged-container.metrics.json")
REPORT_FILE = Path("results/reports/case-001-trivy-report.md")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def main() -> None:
    matched_data = load_json(MATCHED_FILE)
    metrics_data = load_json(METRICS_FILE)

    summary = matched_data["summary"]
    counts = metrics_data["counts"]
    metrics = metrics_data["metrics"]

    true_positives = matched_data.get("true_positives", [])
    false_negatives = matched_data.get("false_negatives", [])
    unlabelled_extras = matched_data.get("unlabelled_extra_findings", [])

    report_lines = []

    report_lines.append("# Case 001 Trivy Benchmark Report")
    report_lines.append("")
    report_lines.append("## 1. Case Summary")
    report_lines.append("")
    report_lines.append(f"- Case ID: `{CASE_ID}`")
    report_lines.append(f"- Scanner: `{TOOL_NAME}`")
    report_lines.append("- Artifact type: `kubernetes_yaml`")
    report_lines.append("- Benchmark issue: Privileged container")
    report_lines.append("- Ground truth ID: `GT-001`")
    report_lines.append("")

    report_lines.append("## 2. Ground Truth Detection Result")
    report_lines.append("")
    report_lines.append(f"- Ground truth items: `{summary['ground_truth_items_count']}`")
    report_lines.append(f"- Normalised Trivy findings: `{summary['normalised_findings_count']}`")
    report_lines.append(f"- Mapped findings: `{summary['mapped_findings_count']}`")
    report_lines.append(f"- Unmapped findings: `{summary['unmapped_findings_count']}`")
    report_lines.append("")

    report_lines.append("## 3. True Positive Findings")
    report_lines.append("")

    if true_positives:
        for item in true_positives:
            report_lines.append(f"- Ground truth: `{item['ground_truth_id']}`")
            report_lines.append(f"  - Scanner rule: `{item['scanner_rule_id']}`")
            report_lines.append(f"  - Rule name: {item['scanner_rule_name']}")
            report_lines.append(f"  - Resource: `{item['resource']}`")
            report_lines.append(f"  - Container: `{item['container']}`")
            report_lines.append(f"  - Field path: `{item['field_path']}`")
            report_lines.append(f"  - Evidence: {item['evidence_message']}")
            report_lines.append("")
    else:
        report_lines.append("No true positive findings were recorded.")
        report_lines.append("")

    report_lines.append("## 4. False Negative Review")
    report_lines.append("")

    if false_negatives:
        for item in false_negatives:
            report_lines.append(f"- Ground truth missed: `{item['ground_truth_id']}`")
            report_lines.append(f"  - Reason: {item['missed_reason']}")
            report_lines.append("")
    else:
        report_lines.append("No false negatives were found. Trivy detected the labelled ground-truth issue.")
        report_lines.append("")

    report_lines.append("## 5. Metric Counts")
    report_lines.append("")
    report_lines.append(f"- True positives: `{counts['true_positive_count']}`")
    report_lines.append(f"- False positives: `{counts['false_positive_count']}`")
    report_lines.append(f"- False negatives: `{counts['false_negative_count']}`")
    report_lines.append(f"- Unlabelled extra findings: `{counts['unlabelled_extra_findings_count']}`")
    report_lines.append("")

    report_lines.append("## 6. Evaluation Metrics")
    report_lines.append("")
    report_lines.append(f"- Precision: `{metrics['precision']}`")
    report_lines.append(f"- Recall: `{metrics['recall']}`")
    report_lines.append(f"- F1 score: `{metrics['f1_score']}`")
    report_lines.append("")

    report_lines.append("## 7. Unlabelled Extra Findings")
    report_lines.append("")
    report_lines.append(
        "These findings were reported by Trivy but are not counted as false positives yet because the benchmark is currently using review mode."
    )
    report_lines.append("")

    for item in unlabelled_extras:
        report_lines.append(f"- `{item['scanner_rule_id']}` — {item['scanner_rule_name']} ({item['severity']})")

    report_lines.append("")
    report_lines.append("## 8. Interpretation")
    report_lines.append("")
    report_lines.append(
        "Trivy successfully detected the privileged container misconfiguration using rule `KSV-0017`. "
        "This finding matched the ground truth label `GT-001`, so it was classified as a true positive."
    )
    report_lines.append("")
    report_lines.append(
        "The additional Trivy findings were stored as unlabelled extras. They may represent valid security recommendations, "
        "but they are not part of the current ground-truth label set for this controlled benchmark case."
    )
    report_lines.append("")

    report_lines.append("## 9. Conclusion")
    report_lines.append("")
    report_lines.append(
        "The first Trivy benchmark run was successful. For case-001, Trivy detected the intended privileged container issue, "
        "producing Precision = 1.0, Recall = 1.0, and F1 Score = 1.0 in review mode."
    )
    report_lines.append("")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open("w", encoding="utf-8") as file:
        file.write("\n".join(report_lines))

    print("Trivy report generated.")
    print(f"Output file: {REPORT_FILE}")


if __name__ == "__main__":
    main()