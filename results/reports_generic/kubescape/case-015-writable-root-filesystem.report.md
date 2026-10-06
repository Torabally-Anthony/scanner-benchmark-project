# Benchmark Report: Kubescape

**Case:** `case-015-writable-root-filesystem`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 5 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 4 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.2 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.3333 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-015 | WritableRootFilesystem | Pod.benchmark.writable-root-filesystem-demo | Detected | C-0017 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-015-writable-root-filesystem-0001 | C-0017 | GT-015 | Pod.benchmark.writable-root-filesystem-demo |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-015-writable-root-filesystem-0002 | C-0073 | Unknown |
| kubescape-case-015-writable-root-filesystem-0003 | C-0077 | Unknown |
| kubescape-case-015-writable-root-filesystem-0004 | C-0211 | Unknown |
| kubescape-case-015-writable-root-filesystem-0005 | C-0237 | Unknown |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-015-writable-root-filesystem.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-015-writable-root-filesystem.metrics.json`
- Generated: `2026-10-02T10:32:22.385287+00:00`
