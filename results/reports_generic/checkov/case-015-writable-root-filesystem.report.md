# Benchmark Report: Checkov

**Case:** `case-015-writable-root-filesystem`

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
| GT-015 | WritableRootFilesystem | Pod.benchmark.writable-root-filesystem-demo | Detected | CKV_K8S_22 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-015-writable-root-filesystem-0001 | CKV_K8S_22 | GT-015 | Pod.benchmark.writable-root-filesystem-demo |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-015-writable-root-filesystem-0002 | CKV_K8S_43 | Pod.benchmark.writable-root-filesystem-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-015-writable-root-filesystem.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-015-writable-root-filesystem.metrics.json`
- Generated: `2026-10-21T11:14:16.217089+00:00`
