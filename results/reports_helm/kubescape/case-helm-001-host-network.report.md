# Benchmark Report: Kubescape

**Case:** `case-helm-001-host-network`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `v4.0.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 6 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 5 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.1667 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.2857 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-001 | HostNetwork | Deployment.scanner-benchmark.helm-host-network-demo-app | Detected | C-0041 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-helm-001-host-network-0002 | C-0041 | GT-HELM-001 | Deployment.scanner-benchmark.helm-host-network-demo-app |

## False positives (5)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-001-host-network-0001 | C-0030 | Unknown |
| kubescape-case-helm-001-host-network-0003 | C-0077 | Unknown |
| kubescape-case-helm-001-host-network-0004 | C-0211 | Unknown |
| kubescape-case-helm-001-host-network-0005 | C-0237 | Unknown |
| kubescape-case-helm-001-host-network-0006 | C-0260 | Unknown |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-001-host-network.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-001-host-network.metrics.json`
- Generated: `2026-09-17T06:59:44.635882+00:00`
