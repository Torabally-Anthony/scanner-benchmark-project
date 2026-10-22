# Benchmark Report: Checkov

**Case:** `case-helm-012-latest-image-tag`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

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
| GT-HELM-012 | MutableImageReference | Deployment.benchmark.latest-image-tag-helm-demo | Detected | CKV_K8S_14 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-helm-012-latest-image-tag-0001 | CKV_K8S_14 | GT-HELM-012 | Deployment.benchmark.latest-image-tag-helm-demo |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-helm-012-latest-image-tag-0002 | CKV_K8S_43 | Deployment.benchmark.latest-image-tag-helm-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/checkov/case-helm-012-latest-image-tag.matched.json`
- Full metrics: `results/metrics_helm/checkov/case-helm-012-latest-image-tag.metrics.json`
- Generated: `2026-10-17T06:55:46.749173+00:00`
