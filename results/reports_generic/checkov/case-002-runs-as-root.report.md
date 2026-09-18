# Benchmark Report: Checkov

**Case:** `case-002-runs-as-root`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `2.5.20`

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
| GT-002 | RunsAsRoot | Deployment.scanner-benchmark.runs-as-root-demo-app | Detected | CKV_K8S_23 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-002-runs-as-root-0003 | CKV_K8S_23 | GT-002 | Deployment.scanner-benchmark.runs-as-root-demo-app |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-002-runs-as-root-0001 | CKV_K8S_43 | Deployment.scanner-benchmark.runs-as-root-demo-app |
| checkov-case-002-runs-as-root-0002 | CKV_K8S_15 | Deployment.scanner-benchmark.runs-as-root-demo-app |
| checkov-case-002-runs-as-root-0004 | CKV_K8S_40 | Deployment.scanner-benchmark.runs-as-root-demo-app |
| checkov-case-002-runs-as-root-0005 | CKV2_K8S_6 | Pod.default.runs-as-root-demo-app.app-runs-as-root-demo-app |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-002-runs-as-root.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-002-runs-as-root.metrics.json`
- Generated: `2026-09-17T06:59:44.010601+00:00`
