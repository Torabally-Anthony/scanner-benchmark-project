# Benchmark Report: Kubescape

**Case:** `case-002-runs-as-root`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

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
| GT-002 | RunsAsRoot | Deployment.scanner-benchmark.runs-as-root-demo-app | Detected | C-0013 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-002-runs-as-root-0001 | C-0013 | GT-002 | Deployment.scanner-benchmark.runs-as-root-demo-app |

## False positives (5)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-002-runs-as-root-0002 | C-0030 | Unknown |
| kubescape-case-002-runs-as-root-0003 | C-0077 | Unknown |
| kubescape-case-002-runs-as-root-0004 | C-0211 | Unknown |
| kubescape-case-002-runs-as-root-0005 | C-0237 | Unknown |
| kubescape-case-002-runs-as-root-0006 | C-0260 | Unknown |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-002-runs-as-root.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-002-runs-as-root.metrics.json`
- Generated: `2026-09-17T06:59:44.122614+00:00`
