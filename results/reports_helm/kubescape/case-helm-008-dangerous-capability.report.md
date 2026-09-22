# Benchmark Report: Kubescape

**Case:** `case-helm-008-dangerous-capability`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 22 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 21 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0455 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.087 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-008 | DangerousCapability | Deployment.default.capability-helm-demo | Detected | C-0046 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-helm-008-dangerous-capability-0007 | C-0046 | GT-HELM-008 | Deployment.default.capability-helm-demo |

## False positives (21)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-008-dangerous-capability-0001 | C-0004 | Unknown |
| kubescape-case-helm-008-dangerous-capability-0002 | C-0009 | Unknown |
| kubescape-case-helm-008-dangerous-capability-0003 | C-0013 | Unknown |
| kubescape-case-helm-008-dangerous-capability-0004 | C-0017 | Unknown |
| kubescape-case-helm-008-dangerous-capability-0005 | C-0018 | Unknown |

Showing 5 of 21. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-008-dangerous-capability.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-008-dangerous-capability.metrics.json`
- Generated: `2026-09-22T12:10:58.083389+00:00`
