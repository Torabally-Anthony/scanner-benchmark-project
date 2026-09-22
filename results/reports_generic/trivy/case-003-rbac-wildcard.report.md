# Benchmark Report: Trivy

**Case:** `case-003-rbac-wildcard`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 2 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 1 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.5 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.6667 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-003 | RBACWildcard | Role.benchmark.wildcard-role | Detected | KSV-0044 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-003-rbac-wildcard-0001 | KSV-0044 | GT-003 | Role.benchmark.wildcard-role |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-003-rbac-wildcard-0002 | KSV-0112 | artifact.yaml |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-003-rbac-wildcard.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-003-rbac-wildcard.metrics.json`
- Generated: `2026-09-22T12:10:27.338173+00:00`
