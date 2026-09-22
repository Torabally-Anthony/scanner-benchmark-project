# Benchmark Report: Checkov

**Case:** `case-006-latest-image-tag`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

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
| GT-006 | UnpinnedImage | Deployment.benchmark.latest-tag-demo | Detected | CKV_K8S_14 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-006-latest-image-tag-0004 | CKV_K8S_14 | GT-006 | Deployment.benchmark.latest-tag-demo |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-006-latest-image-tag-0001 | CKV_K8S_8 | Deployment.benchmark.latest-tag-demo |
| checkov-case-006-latest-image-tag-0002 | CKV_K8S_9 | Deployment.benchmark.latest-tag-demo |
| checkov-case-006-latest-image-tag-0003 | CKV_K8S_29 | Deployment.benchmark.latest-tag-demo |
| checkov-case-006-latest-image-tag-0005 | CKV_K8S_43 | Deployment.benchmark.latest-tag-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-006-latest-image-tag.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-006-latest-image-tag.metrics.json`
- Generated: `2026-09-22T12:10:29.528859+00:00`
