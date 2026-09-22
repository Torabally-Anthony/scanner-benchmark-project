# Benchmark Report: Trivy

**Case:** `case-helm-005-host-ipc`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 11 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 10 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0909 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.1667 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-005 | HostIPC | Deployment.default.host-ipc-demo | Detected | KSV-0008 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-helm-005-host-ipc-0001 | KSV-0008 | GT-HELM-005 | Deployment.default.host-ipc-demo |

## False positives (10)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-helm-005-host-ipc-0002 | KSV-0011 | templates/deployment.yaml |
| trivy-case-helm-005-host-ipc-0003 | KSV-0014 | templates/deployment.yaml |
| trivy-case-helm-005-host-ipc-0004 | KSV-0015 | templates/deployment.yaml |
| trivy-case-helm-005-host-ipc-0005 | KSV-0016 | templates/deployment.yaml |
| trivy-case-helm-005-host-ipc-0006 | KSV-0018 | templates/deployment.yaml |

Showing 5 of 10. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/trivy/case-helm-005-host-ipc.matched.json`
- Full metrics: `results/metrics_helm/trivy/case-helm-005-host-ipc.metrics.json`
- Generated: `2026-09-22T12:10:55.457050+00:00`
