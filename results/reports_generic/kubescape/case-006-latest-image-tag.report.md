# Benchmark Report: Kubescape

**Case:** `case-006-latest-image-tag`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 9 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 9 |
| False negatives | 1 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0 |
| Recall | TP / (TP + FN) | 0 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-006 | UnpinnedImage | Deployment.benchmark.latest-tag-demo | Missed | — |

## False positives (9)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-006-latest-image-tag-0001 | C-0013 | Unknown |
| kubescape-case-006-latest-image-tag-0002 | C-0018 | Unknown |
| kubescape-case-006-latest-image-tag-0003 | C-0030 | Unknown |
| kubescape-case-006-latest-image-tag-0004 | C-0056 | Unknown |
| kubescape-case-006-latest-image-tag-0005 | C-0076 | Unknown |

Showing 5 of 9. See the matched JSON for the full list.

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-006 | UnpinnedImage | Deployment.benchmark.latest-tag-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-006-latest-image-tag.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-006-latest-image-tag.metrics.json`
- Generated: `2026-09-22T12:10:30.108813+00:00`
