# Benchmark Report: Kubescape

**Case:** `case-helm-012-latest-image-tag`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 3 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 3 |
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
| GT-HELM-012 | MutableImageReference | Deployment.benchmark.latest-image-tag-helm-demo | Missed | — |

## False positives (3)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-012-latest-image-tag-0001 | C-0077 | Unknown |
| kubescape-case-helm-012-latest-image-tag-0002 | C-0211 | Unknown |
| kubescape-case-helm-012-latest-image-tag-0003 | C-0237 | Unknown |

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-HELM-012 | MutableImageReference | Deployment.benchmark.latest-image-tag-helm-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-012-latest-image-tag.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-012-latest-image-tag.metrics.json`
- Generated: `2026-09-26T16:07:29.156614+00:00`
