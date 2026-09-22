# Benchmark Report: Kubescape

**Case:** `case-helm-009-privilege-escalation`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 21 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 20 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
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
| GT-HELM-009 | PrivilegeEscalation | Deployment.default.escalation-helm-demo | Detected | C-0016 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-helm-009-privilege-escalation-0004 | C-0016 | GT-HELM-009 | Deployment.default.escalation-helm-demo |

## False positives (20)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-009-privilege-escalation-0001 | C-0004 | Unknown |
| kubescape-case-helm-009-privilege-escalation-0002 | C-0009 | Unknown |
| kubescape-case-helm-009-privilege-escalation-0003 | C-0013 | Unknown |
| kubescape-case-helm-009-privilege-escalation-0005 | C-0017 | Unknown |
| kubescape-case-helm-009-privilege-escalation-0006 | C-0018 | Unknown |

Showing 5 of 20. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-009-privilege-escalation.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-009-privilege-escalation.metrics.json`
- Generated: `2026-09-22T12:10:58.904013+00:00`
