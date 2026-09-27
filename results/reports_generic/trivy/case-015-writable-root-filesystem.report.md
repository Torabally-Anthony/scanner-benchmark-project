# Benchmark Report: Trivy

**Case:** `case-015-writable-root-filesystem`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 1 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 0 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 1 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 1 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-015 | WritableRootFilesystem | Pod.benchmark.writable-root-filesystem-demo | Detected | KSV-0014 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-015-writable-root-filesystem-0001 | KSV-0014 | GT-015 | Pod.benchmark.writable-root-filesystem-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-015-writable-root-filesystem.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-015-writable-root-filesystem.metrics.json`
- Generated: `2026-09-26T15:47:05.799084+00:00`
