# Benchmark Report: Kubescape

**Case:** `case-019-unconfined-seccomp`

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
| GT-019 | UnconfinedSeccomp | Pod.benchmark.unconfined-seccomp-demo | Detected | C-0210 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-019-unconfined-seccomp-0003 | C-0210 | GT-019 | Pod.benchmark.unconfined-seccomp-demo |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-019-unconfined-seccomp-0001 | C-0073 | Unknown |
| kubescape-case-019-unconfined-seccomp-0002 | C-0077 | Unknown |
| kubescape-case-019-unconfined-seccomp-0004 | C-0211 | Unknown |
| kubescape-case-019-unconfined-seccomp-0005 | C-0237 | Unknown |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-019-unconfined-seccomp.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-019-unconfined-seccomp.metrics.json`
- Generated: `2026-09-26T15:47:09.210469+00:00`
