# Benchmark Report: Kubescape

**Case:** `case-helm-018-unconfined-seccomp`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 4 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 3 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.25 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.4 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-018 | UnconfinedSeccomp | Deployment.benchmark.unconfined-seccomp-helm-demo | Detected | C-0210 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-helm-018-unconfined-seccomp-0002 | C-0210 | GT-HELM-018 | Deployment.benchmark.unconfined-seccomp-helm-demo |

## False positives (3)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-018-unconfined-seccomp-0001 | C-0077 | Unknown |
| kubescape-case-helm-018-unconfined-seccomp-0003 | C-0211 | Unknown |
| kubescape-case-helm-018-unconfined-seccomp-0004 | C-0237 | Unknown |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-018-unconfined-seccomp.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-018-unconfined-seccomp.metrics.json`
- Generated: `2026-09-26T16:07:33.598541+00:00`
