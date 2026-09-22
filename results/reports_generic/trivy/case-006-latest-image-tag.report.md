# Benchmark Report: Trivy

**Case:** `case-006-latest-image-tag`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 3 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 2 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.3333 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.5 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-006 | UnpinnedImage | Deployment.benchmark.latest-tag-demo | Detected | KSV-0013 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-006-latest-image-tag-0001 | KSV-0013 | GT-006 | Deployment.benchmark.latest-tag-demo |

## False positives (2)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-006-latest-image-tag-0002 | KSV-0021 | artifact.yaml |
| trivy-case-006-latest-image-tag-0003 | KSV-0118 | artifact.yaml |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-006-latest-image-tag.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-006-latest-image-tag.metrics.json`
- Generated: `2026-09-22T12:10:29.802447+00:00`
