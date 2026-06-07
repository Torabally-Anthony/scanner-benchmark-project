from pathlib import Path
import json


MATCHED_FILE = Path(
    "results/matched/checkov/case-001-privileged-container.matched.json"
)

OUTPUT_DIR = Path("results/metrics/checkov")
OUTPUT_FILE = OUTPUT_DIR / "case-001-privileged-container.metrics.json"


def load_json(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing matched file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def safe_divide(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)


def main():
    print("Calculating Checkov metrics...")

    matched_data = load_json(MATCHED_FILE)
    summary = matched_data.get("summary", {})

    tp = summary.get("true_positive_count", 0)
    fp = summary.get("false_positive_count", 0)
    fn = summary.get("false_negative_count", 0)

    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1_score = calculate_f1(precision, recall)

    output = {
        "case_id": matched_data.get("case_id"),
        "tool": matched_data.get("tool"),
        "artifact_type": matched_data.get("artifact_type"),
        "matching_mode": matched_data.get("matching_mode"),

        "counts": {
            "true_positive_count": tp,
            "false_positive_count": fp,
            "false_negative_count": fn,
            "unlabelled_extra_findings_count": summary.get(
                "unlabelled_extra_findings_count", 0
            ),
        },

        "metrics": {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4),
        },

        "formula_used": {
            "precision": "TP / (TP + FP)",
            "recall": "TP / (TP + FN)",
            "f1_score": "2 * (Precision * Recall) / (Precision + Recall)",
        },
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print(f"Metrics output saved to: {OUTPUT_FILE}")
    print(f"TP: {tp}")
    print(f"FP: {fp}")
    print(f"FN: {fn}")
    print(f"Precision: {round(precision, 4)}")
    print(f"Recall: {round(recall, 4)}")
    print(f"F1 Score: {round(f1_score, 4)}")


if __name__ == "__main__":
    main()