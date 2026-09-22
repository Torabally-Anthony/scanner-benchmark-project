# Benchmark Report: Checkov

**Case:** `case-010-dangerous-capability`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 7 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 6 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.1429 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.25 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-010 | DangerousCapability | Deployment.benchmark.dangerous-capability-demo | Detected | CKV_K8S_39 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-010-dangerous-capability-0003 | CKV_K8S_39 | GT-010 | Deployment.benchmark.dangerous-capability-demo |

## False positives (6)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-010-dangerous-capability-0001 | CKV_K8S_8 | Deployment.benchmark.dangerous-capability-demo |
| checkov-case-010-dangerous-capability-0002 | CKV_K8S_15 | Deployment.benchmark.dangerous-capability-demo |
| checkov-case-010-dangerous-capability-0004 | CKV_K8S_9 | Deployment.benchmark.dangerous-capability-demo |
| checkov-case-010-dangerous-capability-0005 | CKV_K8S_25 | Deployment.benchmark.dangerous-capability-demo |
| checkov-case-010-dangerous-capability-0006 | CKV_K8S_29 | Deployment.benchmark.dangerous-capability-demo |

Showing 5 of 6. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-010-dangerous-capability.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-010-dangerous-capability.metrics.json`
- Generated: `2026-09-22T12:10:32.731985+00:00`
