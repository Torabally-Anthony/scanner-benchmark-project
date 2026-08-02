from pathlib import Path
import json


CASE_ID = "case-001-privileged-container"
TOOL_NAME = "trivy"

MATCHED_FILE = Path("results/matched/trivy/case-001-privileged-container.matched.json")
OUTPUT_FILE = Path("results/metrics/trivy/case-001-privileged-container.metrics.json")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def safe_divide(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_f1_score(precision: float, recall: float) -> float:
    denominator = precision + recall

    if denominator == 0:
        return 0.0

    return 2 * (precision * recall) / denominator


def main() -> None:
    matched_data = load_json(MATCHED_FILE)
    summary = matched_data.get("summary", {})

    true_positive_count = summary.get("true_positive_count", 0)
    false_positive_count = summary.get("false_positive_count", 0)
    false_negative_count = summary.get("false_negative_count", 0)
    unlabelled_extra_findings_count = summary.get("unlabelled_extra_findings_count", 0)

    precision = safe_divide(
        true_positive_count,
        true_positive_count + false_positive_count,
    )

    recall = safe_divide(
        true_positive_count,
        true_positive_count + false_negative_count,
    )

    f1_score = calculate_f1_score(precision, recall)

    output = {
        "case_id": CASE_ID,
        "tool": TOOL_NAME,
        "source_file": str(MATCHED_FILE),

        "counts": {
            "true_positive_count": true_positive_count,
            "false_positive_count": false_positive_count,
            "false_negative_count": false_negative_count,
            "unlabelled_extra_findings_count": unlabelled_extra_findings_count,
        },

        "metrics": {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4),
        },

        "interpretation": {
            "precision": "Measures how many reported findings were correct.",
            "recall": "Measures how many ground-truth issues were detected.",
            "f1_score": "Balances precision and recall into one effectiveness score.",
            "review_mode_note": "Unmapped findings are stored as unlabelled extras and are not counted as false positives yet.",
        },
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print("Trivy metrics calculation completed.")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 score: {f1_score:.4f}")


if __name__ == "__main__":
    main()