# Benchmark Report: Checkov

**Case:** `case-018-default-namespace`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

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
| GT-018 | DefaultNamespace | Pod.default.default-namespace-demo | Detected | CKV_K8S_21 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-018-default-namespace-0001 | CKV_K8S_21 | GT-018 | Pod.default.default-namespace-demo |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-018-default-namespace-0002 | CKV_K8S_43 | Pod.default.default-namespace-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-018-default-namespace.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-018-default-namespace.metrics.json`
- Generated: `2026-09-26T15:47:07.871610+00:00`
