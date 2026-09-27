# Benchmark Report: Kubescape

**Case:** `case-014-privilege-escalation`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

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
| GT-014 | PrivilegeEscalation | Pod.benchmark.privilege-escalation-demo | Detected | C-0016 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-014-privilege-escalation-0001 | C-0016 | GT-014 | Pod.benchmark.privilege-escalation-demo |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-014-privilege-escalation-0002 | C-0073 | Unknown |
| kubescape-case-014-privilege-escalation-0003 | C-0077 | Unknown |
| kubescape-case-014-privilege-escalation-0004 | C-0211 | Unknown |
| kubescape-case-014-privilege-escalation-0005 | C-0237 | Unknown |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-014-privilege-escalation.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-014-privilege-escalation.metrics.json`
- Generated: `2026-09-26T15:47:05.334172+00:00`
