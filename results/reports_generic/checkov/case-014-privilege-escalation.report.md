# Benchmark Report: Checkov

**Case:** `case-014-privilege-escalation`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 2 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 1 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.5 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.6667 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-014 | PrivilegeEscalation | Pod.benchmark.privilege-escalation-demo | Detected | CKV_K8S_20 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-014-privilege-escalation-0001 | CKV_K8S_20 | GT-014 | Pod.benchmark.privilege-escalation-demo |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-014-privilege-escalation-0002 | CKV_K8S_43 | Pod.benchmark.privilege-escalation-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-014-privilege-escalation.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-014-privilege-escalation.metrics.json`
- Generated: `2026-09-26T15:47:04.876862+00:00`
