# Benchmark Report: Trivy

**Case:** `case-helm-012-latest-image-tag`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

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
| GT-HELM-012 | MutableImageReference | Deployment.benchmark.latest-image-tag-helm-demo | Detected | KSV-0013 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-helm-012-latest-image-tag-0001 | KSV-0013 | GT-HELM-012 | Deployment.benchmark.latest-image-tag-helm-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/trivy/case-helm-012-latest-image-tag.matched.json`
- Full metrics: `results/metrics_helm/trivy/case-helm-012-latest-image-tag.metrics.json`
- Generated: `2026-10-17T06:55:47.013501+00:00`
