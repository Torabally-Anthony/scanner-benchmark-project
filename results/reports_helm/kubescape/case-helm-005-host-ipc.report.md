# Benchmark Report: Kubescape

**Case:** `case-helm-005-host-ipc`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 22 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 20 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 1 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0476 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.0909 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-005 | HostIPC | Deployment.default.host-ipc-demo | Detected | C-0038, C-0276 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-helm-005-host-ipc-0007 | C-0038 | GT-HELM-005 | Deployment.default.host-ipc-demo |

## False positives (20)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-005-host-ipc-0001 | C-0004 | Unknown |
| kubescape-case-helm-005-host-ipc-0002 | C-0009 | Unknown |
| kubescape-case-helm-005-host-ipc-0003 | C-0013 | Unknown |
| kubescape-case-helm-005-host-ipc-0004 | C-0017 | Unknown |
| kubescape-case-helm-005-host-ipc-0005 | C-0018 | Unknown |

Showing 5 of 20. See the matched JSON for the full list.

## Duplicate matches (1)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| kubescape-case-helm-005-host-ipc-0022 | C-0276 | GT-HELM-005 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-005-host-ipc.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-005-host-ipc.metrics.json`
- Generated: `2026-09-22T12:10:55.712693+00:00`
