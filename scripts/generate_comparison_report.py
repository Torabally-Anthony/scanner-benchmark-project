from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

from config_loader import (
    PROJECT_ROOT,
    ConfigurationError,
    load_benchmark_config,
)


SCANNERS = (
    "checkov",
    "trivy",
    "kubescape",
)


ARTIFACT_SETTINGS: dict[str, dict[str, Any]] = {
    "kubernetes_yaml": {
        "label": "Kubernetes YAML",
        "metrics_root": "results/metrics_generic",
        "applicable_scanners": (
            "checkov",
            "trivy",
            "kubescape",
        ),
    },
    "dockerfile": {
        "label": "Dockerfile",
        "metrics_root": "results/metrics_dockerfile",
        "applicable_scanners": (
            "checkov",
            "trivy",
        ),
    },
    "helm_chart": {
        "label": "Helm chart",
        "metrics_root": "results/metrics_helm",
        "applicable_scanners": (
            "checkov",
            "trivy",
            "kubescape",
        ),
    },
}


COUNT_FIELDS = (
    "true_positive_count",
    "false_positive_count",
    "false_negative_count",
    "unlabelled_extra_findings_count",
    "duplicate_match_count",
    "ambiguous_match_count",
)


METRIC_FIELDS = (
    "precision",
    "recall",
    "f1_score",
)


class ComparisonReportError(Exception):
    """Raised when the comparison report cannot be generated."""


# This function parses command-line arguments.
def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Generate a combined comparison report across "
            "Kubernetes YAML, Dockerfile and Helm cases."
        )
    )

    parser.add_argument(
        "--cases",
        nargs="+",
        default=None,
        help=(
            "Optional case IDs to include. "
            "All configured cases are included by default."
        ),
    )

    parser.add_argument(
        "--output-dir",
        default="results/comparison",
        help=(
            "Directory where the JSON and Markdown reports "
            "will be written."
        ),
    )

    return parser.parse_args()


# This function reads one JSON object from disk.
def read_json(path: Path) -> dict[str, Any]:
    """Read one JSON object from disk."""

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            data = json.load(file)

    except FileNotFoundError as error:
        raise ComparisonReportError(
            f"Required metrics file does not exist: {path}"
        ) from error

    except json.JSONDecodeError as error:
        raise ComparisonReportError(
            f"Invalid JSON in {path}: {error}"
        ) from error

    if not isinstance(data, dict):
        raise ComparisonReportError(
            f"Expected a JSON object in {path}."
        )

    return data


# This function resolves and validates the output directory.
def resolve_output_directory(
    value: str,
) -> Path:
    """Resolve and validate the output directory."""

    output_directory = (
        PROJECT_ROOT
        / value
    ).resolve()

    try:
        output_directory.relative_to(
            PROJECT_ROOT.resolve()
        )

    except ValueError as error:
        raise ComparisonReportError(
            "The output directory must remain "
            "inside the benchmark project."
        ) from error

    return output_directory


# This function selects and validates the cases included in the report.
def select_cases(
    configuration: dict[str, Any],
    requested_cases: list[str] | None,
) -> list[tuple[str, dict[str, Any]]]:
    """Select and validate the cases included in the report."""

    cases = configuration.get("cases")

    if not isinstance(cases, dict):
        raise ComparisonReportError(
            "benchmark_config.yaml does not contain "
            "a valid 'cases' mapping."
        )

    selected_ids = (
        requested_cases
        if requested_cases
        else list(cases.keys())
    )

    selected_cases: list[
        tuple[str, dict[str, Any]]
    ] = []

    for case_id in selected_ids:
        case_configuration = cases.get(case_id)

        if not isinstance(
            case_configuration,
            dict,
        ):
            raise ComparisonReportError(
                f"Case '{case_id}' was not found "
                "in benchmark_config.yaml."
            )

        artifact_type = str(
            case_configuration.get(
                "artifact_type",
                "",
            )
        ).strip().lower()

        if artifact_type not in ARTIFACT_SETTINGS:
            raise ComparisonReportError(
                f"Case '{case_id}' uses unsupported "
                f"artifact type '{artifact_type}'."
            )

        selected_cases.append(
            (
                case_id,
                case_configuration,
            )
        )

    artifact_order = {
        "kubernetes_yaml": 0,
        "dockerfile": 1,
        "helm_chart": 2,
    }

    selected_cases.sort(
        key=lambda item: (
            artifact_order[
                str(
                    item[1]["artifact_type"]
                ).strip().lower()
            ],
            item[0],
        )
    )

    return selected_cases


# This function reads a required numeric value.
def require_number(
    mapping: dict[str, Any],
    field_name: str,
    metrics_path: Path,
) -> float:
    """Read a required numeric value."""

    value = mapping.get(field_name)

    if not isinstance(
        value,
        (int, float),
    ):
        raise ComparisonReportError(
            f"'{field_name}' is missing or non-numeric "
            f"in {metrics_path}."
        )

    return float(value)


# This function loads one scanner-case metrics result.
def load_metric_row(
    case_id: str,
    artifact_type: str,
    scanner: str,
) -> dict[str, Any]:
    """Load one scanner-case metrics result."""

    settings = ARTIFACT_SETTINGS[
        artifact_type
    ]

    metrics_root = (
        PROJECT_ROOT
        / settings["metrics_root"]
    )

    metrics_path = (
        metrics_root
        / scanner
        / f"{case_id}.metrics.json"
    )

    data = read_json(
        metrics_path
    )

    counts = data.get("counts")
    metrics = data.get("metrics")

    if not isinstance(counts, dict):
        raise ComparisonReportError(
            f"Missing 'counts' object in {metrics_path}."
        )

    if not isinstance(metrics, dict):
        raise ComparisonReportError(
            f"Missing 'metrics' object in {metrics_path}."
        )

    row: dict[str, Any] = {
        "case_id": case_id,
        "artifact_type": artifact_type,
        "artifact_label": settings["label"],
        "scanner": scanner,
        "applicable": True,
        "metrics_path": str(
            metrics_path.relative_to(
                PROJECT_ROOT
            )
        ),
        "matching_mode": data.get(
            "matching_mode"
        ),
    }

    for field_name in COUNT_FIELDS:
        row[field_name] = int(
            require_number(
                counts,
                field_name,
                metrics_path,
            )
        )

    for field_name in METRIC_FIELDS:
        row[field_name] = require_number(
            metrics,
            field_name,
            metrics_path,
        )

    return row


# This function classifies scanner coverage for one case.
def classify_case_result(
    row: dict[str, Any],
) -> str:
    """Classify scanner coverage for one case."""

    true_positives = row[
        "true_positive_count"
    ]

    false_negatives = row[
        "false_negative_count"
    ]

    # Case status distinguishes full, partial, and missed ground-truth coverage.
    if (
        true_positives > 0
        and false_negatives == 0
    ):
        return "Detected"

    if (
        true_positives > 0
        and false_negatives > 0
    ):
        return "Partial"

    if (
        true_positives == 0
        and false_negatives > 0
    ):
        return "Missed"

    return "No labelled result"


# This function divides safely when the denominator may be zero.
def safe_divide(
    numerator: int,
    denominator: int,
) -> float | None:
    """Divide safely when the denominator may be zero."""

    if denominator == 0:
        return None

    return numerator / denominator


# This function aggregates scanner results across multiple cases.
def aggregate_rows(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate scanner results across multiple cases."""

    total_tp = sum(
        row["true_positive_count"]
        for row in rows
    )

    total_fp = sum(
        row["false_positive_count"]
        for row in rows
    )

    total_fn = sum(
        row["false_negative_count"]
        for row in rows
    )

    # Micro metrics combine all case counts before calculating each score.
    micro_precision = safe_divide(
        total_tp,
        total_tp + total_fp,
    )

    micro_recall = safe_divide(
        total_tp,
        total_tp + total_fn,
    )

    if (
        micro_precision is None
        or micro_recall is None
        or micro_precision + micro_recall == 0
    ):
        micro_f1 = None

    else:
        micro_f1 = (
            2
            * micro_precision
            * micro_recall
            / (
                micro_precision
                + micro_recall
            )
        )

    return {
        "applicable_case_count": len(rows),

        "true_positive_count": total_tp,

        "false_positive_count": total_fp,

        "false_negative_count": total_fn,

        "unlabelled_extra_findings_count": sum(
            row[
                "unlabelled_extra_findings_count"
            ]
            for row in rows
        ),

        "duplicate_match_count": sum(
            row["duplicate_match_count"]
            for row in rows
        ),

        "ambiguous_match_count": sum(
            row["ambiguous_match_count"]
            for row in rows
        ),

        "micro_precision": micro_precision,

        "micro_recall": micro_recall,

        "micro_f1_score": micro_f1,

        # Macro metrics give every case equal weight by averaging its score.
        "macro_precision": (
            mean(
                row["precision"]
                for row in rows
            )
            if rows
            else None
        ),

        "macro_recall": (
            mean(
                row["recall"]
                for row in rows
            )
            if rows
            else None
        ),

        "macro_f1_score": (
            mean(
                row["f1_score"]
                for row in rows
            )
            if rows
            else None
        ),
    }


# This function builds the complete comparison data structure.
def build_report(
    selected_cases: list[
        tuple[str, dict[str, Any]]
    ],
) -> dict[str, Any]:
    """Build the complete comparison data structure."""

    case_results: list[
        dict[str, Any]
    ] = []

    coverage_matrix: list[
        dict[str, Any]
    ] = []

    for (
        case_id,
        case_configuration,
    ) in selected_cases:

        artifact_type = str(
            case_configuration[
                "artifact_type"
            ]
        ).strip().lower()

        settings = ARTIFACT_SETTINGS[
            artifact_type
        ]

        applicable_scanners = set(
            settings[
                "applicable_scanners"
            ]
        )

        coverage_row: dict[str, Any] = {
            "case_id": case_id,
            "artifact_type": artifact_type,
            "artifact_label": settings["label"],
            "scanners": {},
        }

        for scanner in SCANNERS:
            # Non-applicable scanners are excluded rather than treated as missed detections.
            if scanner not in applicable_scanners:
                coverage_row[
                    "scanners"
                ][scanner] = "Not applicable"

                continue

            row = load_metric_row(
                case_id=case_id,
                artifact_type=artifact_type,
                scanner=scanner,
            )

            row["status"] = (
                classify_case_result(row)
            )

            case_results.append(row)

            coverage_row[
                "scanners"
            ][scanner] = row["status"]

        coverage_matrix.append(
            coverage_row
        )

    artifact_summaries: dict[
        str,
        Any,
    ] = {}

    for (
        artifact_type,
        settings,
    ) in ARTIFACT_SETTINGS.items():

        artifact_rows = [
            row
            for row in case_results
            if (
                row["artifact_type"]
                == artifact_type
            )
        ]

        scanner_summaries: dict[
            str,
            Any,
        ] = {}

        for scanner in settings[
            "applicable_scanners"
        ]:
            scanner_rows = [
                row
                for row in artifact_rows
                if row["scanner"] == scanner
            ]

            scanner_summaries[
                scanner
            ] = aggregate_rows(
                scanner_rows
            )

        artifact_case_count = sum(
            1
            for (
                _,
                case_configuration,
            ) in selected_cases
            if (
                str(
                    case_configuration[
                        "artifact_type"
                    ]
                ).strip().lower()
                == artifact_type
            )
        )

        artifact_summaries[
            artifact_type
        ] = {
            "label": settings["label"],
            "case_count": artifact_case_count,
            "scanners": scanner_summaries,
        }

    scanner_summaries: dict[
        str,
        Any,
    ] = {}

    total_case_count = len(
        selected_cases
    )

    for scanner in SCANNERS:
        scanner_rows = [
            row
            for row in case_results
            if row["scanner"] == scanner
        ]

        summary = aggregate_rows(
            scanner_rows
        )

        applicable_count = sum(
            1
            for (
                _,
                case_configuration,
            ) in selected_cases
            if scanner in ARTIFACT_SETTINGS[
                str(
                    case_configuration[
                        "artifact_type"
                    ]
                ).strip().lower()
            ]["applicable_scanners"]
        )

        # Applicability is tracked separately so unsupported cases do not lower scanner scores.
        summary[
            "applicable_case_count"
        ] = applicable_count

        summary[
            "not_applicable_case_count"
        ] = (
            total_case_count
            - applicable_count
        )

        scanner_summaries[
            scanner
        ] = summary

    corpus_summary: dict[
        str,
        Any,
    ] = {}

    for (
        artifact_type,
        settings,
    ) in ARTIFACT_SETTINGS.items():

        case_count = sum(
            1
            for (
                _,
                case_configuration,
            ) in selected_cases
            if (
                str(
                    case_configuration[
                        "artifact_type"
                    ]
                ).strip().lower()
                == artifact_type
            )
        )

        corpus_summary[
            artifact_type
        ] = {
            "label": settings["label"],
            "case_count": case_count,
            "applicable_scanners": list(
                settings[
                    "applicable_scanners"
                ]
            ),
        }

    return {
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),

        "case_count": total_case_count,

        "scanner_case_result_count": len(
            case_results
        ),

        "corpus_summary": corpus_summary,

        "case_results": case_results,

        "coverage_matrix": coverage_matrix,

        "artifact_summaries": (
            artifact_summaries
        ),

        "scanner_summaries": (
            scanner_summaries
        ),
    }


# This function formats one metric for Markdown.
def format_metric(
    value: Any,
) -> str:
    """Format one metric for Markdown."""

    if value is None:
        return "N/A"

    return f"{float(value):.4f}"


# This function builds a Markdown table.
def markdown_table(
    headers: list[str],
    rows: list[list[Any]],
) -> list[str]:
    """Build a Markdown table."""

    output = [
        "| "
        + " | ".join(headers)
        + " |",

        "| "
        + " | ".join(
            "---"
            for _ in headers
        )
        + " |",
    ]

    for row in rows:
        output.append(
            "| "
            + " | ".join(
                str(value)
                for value in row
            )
            + " |"
        )

    return output


# This function renders the comparison report as Markdown.
def render_markdown(
    report: dict[str, Any],
) -> str:
    """Render the comparison report as Markdown."""

    lines = [
        "# Benchmark Comparison Report",
        "",
        (
            "Generated: "
            f"`{report['generated_at_utc']}`"
        ),
        "",
        "## Methodology note",
        "",
        (
            "Metrics are aggregated only across "
            "scanner–artifact combinations that are "
            "applicable."
        ),
        "",
        (
            "Kubescape is marked **Not applicable** "
            "for Dockerfile cases and is not assigned "
            "false negatives for them."
        ),
        "",
        (
            "In review mode, unlabelled extra findings "
            "are reported as review burden and are not "
            "automatically counted as false positives."
        ),
        "",
        "## Corpus overview",
        "",
    ]

    corpus_rows: list[list[Any]] = []

    for artifact_type in (
        "kubernetes_yaml",
        "dockerfile",
        "helm_chart",
    ):
        summary = report[
            "corpus_summary"
        ][artifact_type]

        corpus_rows.append(
            [
                summary["label"],
                summary["case_count"],
                ", ".join(
                    summary[
                        "applicable_scanners"
                    ]
                ),
            ]
        )

    lines.extend(
        markdown_table(
            [
                "Artifact family",
                "Cases",
                "Applicable scanners",
            ],
            corpus_rows,
        )
    )

    lines.extend(
        [
            "",
            "## Per-case results",
            "",
        ]
    )

    per_case_rows = []

    for row in report[
        "case_results"
    ]:
        per_case_rows.append(
            [
                row["case_id"],
                row["artifact_label"],
                row["scanner"],
                row[
                    "true_positive_count"
                ],
                row[
                    "false_positive_count"
                ],
                row[
                    "false_negative_count"
                ],
                row[
                    "unlabelled_extra_findings_count"
                ],
                format_metric(
                    row["precision"]
                ),
                format_metric(
                    row["recall"]
                ),
                format_metric(
                    row["f1_score"]
                ),
            ]
        )

    lines.extend(
        markdown_table(
            [
                "Case",
                "Artifact",
                "Scanner",
                "TP",
                "FP",
                "FN",
                "Extras",
                "Precision",
                "Recall",
                "F1",
            ],
            per_case_rows,
        )
    )

    lines.extend(
        [
            "",
            "## Scanner coverage matrix",
            "",
        ]
    )

    coverage_rows = []

    for row in report[
        "coverage_matrix"
    ]:
        coverage_rows.append(
            [
                row["case_id"],
                row["artifact_label"],
                row[
                    "scanners"
                ]["checkov"],
                row[
                    "scanners"
                ]["trivy"],
                row[
                    "scanners"
                ]["kubescape"],
            ]
        )

    lines.extend(
        markdown_table(
            [
                "Case",
                "Artifact",
                "Checkov",
                "Trivy",
                "Kubescape",
            ],
            coverage_rows,
        )
    )

    lines.extend(
        [
            "",
            "## Results by artifact family",
            "",
        ]
    )

    for artifact_type in (
        "kubernetes_yaml",
        "dockerfile",
        "helm_chart",
    ):
        artifact_summary = report[
            "artifact_summaries"
        ][artifact_type]

        lines.extend(
            [
                (
                    "### "
                    + artifact_summary[
                        "label"
                    ]
                ),
                "",
            ]
        )

        artifact_rows = []

        for (
            scanner,
            summary,
        ) in artifact_summary[
            "scanners"
        ].items():

            artifact_rows.append(
                [
                    scanner,
                    summary[
                        "applicable_case_count"
                    ],
                    summary[
                        "true_positive_count"
                    ],
                    summary[
                        "false_positive_count"
                    ],
                    summary[
                        "false_negative_count"
                    ],
                    summary[
                        "unlabelled_extra_findings_count"
                    ],
                    format_metric(
                        summary[
                            "micro_precision"
                        ]
                    ),
                    format_metric(
                        summary[
                            "micro_recall"
                        ]
                    ),
                    format_metric(
                        summary[
                            "micro_f1_score"
                        ]
                    ),
                    format_metric(
                        summary[
                            "macro_f1_score"
                        ]
                    ),
                ]
            )

        lines.extend(
            markdown_table(
                [
                    "Scanner",
                    "Cases",
                    "TP",
                    "FP",
                    "FN",
                    "Extras",
                    "Micro P",
                    "Micro R",
                    "Micro F1",
                    "Macro F1",
                ],
                artifact_rows,
            )
        )

        lines.append("")

    lines.extend(
        [
            "## Overall scanner summary",
            "",
        ]
    )

    overall_rows = []

    for scanner in SCANNERS:
        summary = report[
            "scanner_summaries"
        ][scanner]

        overall_rows.append(
            [
                scanner,
                summary[
                    "applicable_case_count"
                ],
                summary[
                    "not_applicable_case_count"
                ],
                summary[
                    "true_positive_count"
                ],
                summary[
                    "false_positive_count"
                ],
                summary[
                    "false_negative_count"
                ],
                summary[
                    "unlabelled_extra_findings_count"
                ],
                format_metric(
                    summary[
                        "micro_precision"
                    ]
                ),
                format_metric(
                    summary[
                        "micro_recall"
                    ]
                ),
                format_metric(
                    summary[
                        "micro_f1_score"
                    ]
                ),
                format_metric(
                    summary[
                        "macro_f1_score"
                    ]
                ),
            ]
        )

    lines.extend(
        markdown_table(
            [
                "Scanner",
                "Applicable cases",
                "N/A cases",
                "TP",
                "FP",
                "FN",
                "Extras",
                "Micro P",
                "Micro R",
                "Micro F1",
                "Macro F1",
            ],
            overall_rows,
        )
    )

    lines.append("")

    return "\n".join(lines)


# This function generates both comparison reports.
def run() -> int:
    """Generate both comparison reports."""

    arguments = parse_arguments()

    configuration = (
        load_benchmark_config()
    )

    selected_cases = select_cases(
        configuration=configuration,
        requested_cases=arguments.cases,
    )

    report = build_report(
        selected_cases
    )

    output_directory = (
        resolve_output_directory(
            arguments.output_dir
        )
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_path = (
        output_directory
        / "benchmark-comparison.json"
    )

    markdown_path = (
        output_directory
        / "benchmark-comparison.md"
    )

    with json_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

        file.write("\n")

    markdown_path.write_text(
        render_markdown(report),
        encoding="utf-8",
    )

    print()
    print(
        "Comparison report generated "
        "successfully."
    )

    print(
        "JSON: "
        + str(
            json_path.relative_to(
                PROJECT_ROOT
            )
        )
    )

    print(
        "Markdown: "
        + str(
            markdown_path.relative_to(
                PROJECT_ROOT
            )
        )
    )

    print(
        "Cases included: "
        + str(
            report["case_count"]
        )
    )

    print(
        "Scanner-case results included: "
        + str(
            report[
                "scanner_case_result_count"
            ]
        )
    )

    return 0


# This function serves as the application entry point and handles any errors.
def main() -> int:
    """Application entry point."""

    try:
        return run()

    except (
        ConfigurationError,
        ComparisonReportError,
    ) as error:
        print()
        print(
            "Comparison report generation failed."
        )
        print(f"Reason: {error}")

        return 1

    except KeyboardInterrupt:
        print()
        print(
            "Comparison report generation cancelled."
        )

        return 130

    except Exception as error:
        print()
        print(
            "Unexpected comparison report error."
        )
        print(
            f"{type(error).__name__}: {error}"
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())
