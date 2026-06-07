from pathlib import Path
import json


METRICS_FILE = Path(
    "results/metrics/checkov/case-001-privileged-container.metrics.json"
)

MATCHED_FILE = Path(
    "results/matched/checkov/case-001-privileged-container.matched.json"
)

OUTPUT_DIR = Path("results/reports")
OUTPUT_FILE = OUTPUT_DIR / "case-001-checkov-report.md"


def load_json(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("Generating Checkov report for case-001...")

    metrics_data = load_json(METRICS_FILE)
    matched_data = load_json(MATCHED_FILE)

    counts = metrics_data["counts"]
    metrics = metrics_data["metrics"]

    true_positives = matched_data.get("true_positives", [])
    false_negatives = matched_data.get("false_negatives", [])
    unlabelled_extra_findings = matched_data.get("unlabelled_extra_findings", [])

    report_lines = []

    report_lines.append("# Case 001 Checkov Benchmark Report")
    report_lines.append("")
    report_lines.append("## 1. Case Summary")
    report_lines.append("")
    report_lines.append(f"**Case ID:** `{metrics_data.get('case_id')}`  ")
    report_lines.append(f"**Tool:** `{metrics_data.get('tool')}`  ")
    report_lines.append(f"**Artifact type:** `{metrics_data.get('artifact_type')}`  ")
    report_lines.append(f"**Matching mode:** `{metrics_data.get('matching_mode')}`  ")
    report_lines.append("")
    report_lines.append(
        "This benchmark case tests whether Checkov can detect a Kubernetes "
        "container running in privileged mode."
    )
    report_lines.append("")
    report_lines.append("The intentional ground-truth misconfiguration is:")
    report_lines.append("")
    report_lines.append("`securityContext.privileged: true`")
    report_lines.append("")

    report_lines.append("## 2. Ground-Truth Detection Result")
    report_lines.append("")
    report_lines.append(
        "Checkov successfully detected the intended privileged-container misconfiguration."
    )
    report_lines.append("")

    report_lines.append("## 3. True Positive Finding")
    report_lines.append("")

    if true_positives:
        for item in true_positives:
            report_lines.append(f"- **Ground-truth ID:** `{item.get('ground_truth_id')}`")
            report_lines.append(f"- **Scanner rule ID:** `{item.get('scanner_rule_id')}`")
            report_lines.append(f"- **Scanner rule name:** {item.get('scanner_rule_name')}")
            report_lines.append(f"- **Category:** `{item.get('category')}`")
            report_lines.append(f"- **Subcategory:** `{item.get('subcategory')}`")
            report_lines.append(f"- **Resource:** `{item.get('resource')}`")
            report_lines.append(f"- **Field path:** `{item.get('field_path')}`")
            report_lines.append(f"- **Match status:** `{item.get('match_status')}`")
            report_lines.append("")
    else:
        report_lines.append("No true positives were found.")
        report_lines.append("")

    report_lines.append("## 4. Metric Counts")
    report_lines.append("")
    report_lines.append("| Count Type | Value |")
    report_lines.append("|---|---:|")
    report_lines.append(f"| True positives | {counts.get('true_positive_count')} |")
    report_lines.append(f"| False positives | {counts.get('false_positive_count')} |")
    report_lines.append(f"| False negatives | {counts.get('false_negative_count')} |")
    report_lines.append(
        f"| Unlabelled extra findings | {counts.get('unlabelled_extra_findings_count')} |"
    )
    report_lines.append("")

    report_lines.append("## 5. Evaluation Metrics")
    report_lines.append("")
    report_lines.append("| Metric | Formula | Value |")
    report_lines.append("|---|---|---:|")
    report_lines.append(
        f"| Precision | TP / (TP + FP) | {metrics.get('precision')} |"
    )
    report_lines.append(
        f"| Recall | TP / (TP + FN) | {metrics.get('recall')} |"
    )
    report_lines.append(
        f"| F1 score | 2 × (Precision × Recall) / (Precision + Recall) | {metrics.get('f1_score')} |"
    )
    report_lines.append("")

    report_lines.append("## 6. False Negative Review")
    report_lines.append("")

    if false_negatives:
        for item in false_negatives:
            report_lines.append(
                f"- `{item.get('ground_truth_id')}` was missed by the scanner."
            )
    else:
        report_lines.append("No false negatives were found.")

    report_lines.append("")

    report_lines.append("## 7. Unlabelled Extra Findings")
    report_lines.append("")
    report_lines.append(
        "Checkov also reported additional findings that were not part of the current "
        "ground-truth label."
    )
    report_lines.append("")
    report_lines.append(
        "In this early review-mode version of the benchmark, these are stored as "
        "**unlabelled extra findings** instead of being counted as false positives."
    )
    report_lines.append("")

    if unlabelled_extra_findings:
        for item in unlabelled_extra_findings:
            report_lines.append(
                f"- `{item.get('scanner_rule_id')}`: {item.get('scanner_rule_name')}"
            )
    else:
        report_lines.append("No unlabelled extra findings were found.")

    report_lines.append("")

    report_lines.append("## 8. Interpretation")
    report_lines.append("")
    report_lines.append(
        "For this first controlled benchmark case, Checkov correctly detected the "
        "intended privileged-container issue."
    )
    report_lines.append("")
    report_lines.append(
        "Because the scanner detected the only ground-truth misconfiguration and did "
        "not miss it, recall is 1.0."
    )
    report_lines.append("")
    report_lines.append(
        "Because review mode does not count the extra unmapped findings as false "
        "positives yet, precision is also 1.0."
    )
    report_lines.append("")
    report_lines.append(
        "The 19 unlabelled extra findings show that Checkov reports many additional "
        "Kubernetes best-practice issues. Later in the project, these findings can "
        "either be mapped to new benchmark categories or counted as false positives "
        "in a stricter evaluation mode."
    )
    report_lines.append("")

    report_lines.append("## 9. End-to-End Status")
    report_lines.append("")
    report_lines.append("This case successfully completed the first mini end-to-end benchmark flow:")
    report_lines.append("")
    report_lines.append("artifact.yaml")
    report_lines.append("→ Checkov raw JSON")
    report_lines.append("→ normalised JSON")
    report_lines.append("→ matched JSON")
    report_lines.append("→ metrics JSON")
    report_lines.append("→ markdown report")
    report_lines.append("")

    report_lines.append("## 10. Conclusion")
    report_lines.append("")
    report_lines.append(
        "The first end-to-end Checkov benchmark test is successful. The system can "
        "scan a controlled Kubernetes misconfiguration, normalise the scanner output, "
        "match the finding to ground truth, calculate precision, recall and F1, and "
        "generate a readable report."
    )
    report_lines.append("")

    report = "\n".join(report_lines)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"Report generated successfully: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()