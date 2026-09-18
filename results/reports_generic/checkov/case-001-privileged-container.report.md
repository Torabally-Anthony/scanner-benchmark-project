# Benchmark Report: Checkov

**Case:** `case-001-privileged-container`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `2.5.20`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 20 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 19 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.05 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.0952 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-001 | PrivilegedContainer | Deployment.default.privileged-demo-app | Detected | CKV_K8S_16 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-001-privileged-container-0013 | CKV_K8S_16 | GT-001 | Deployment.default.privileged-demo-app |

## False positives (19)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-001-privileged-container-0001 | CKV_K8S_20 | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0002 | CKV_K8S_11 | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0003 | CKV_K8S_10 | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0004 | CKV_K8S_21 | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0005 | CKV_K8S_28 | Deployment.default.privileged-demo-app |

Showing 5 of 19. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-001-privileged-container.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-001-privileged-container.metrics.json`
- Generated: `2026-09-17T06:59:43.954172+00:00`
