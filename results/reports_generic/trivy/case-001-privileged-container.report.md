# Benchmark Report: Trivy

**Case:** `case-001-privileged-container`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 18 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 17 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0556 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.1053 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-001 | PrivilegedContainer | Deployment.default.privileged-demo-app | Detected | KSV-0017 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-001-privileged-container-0009 | KSV-0017 | GT-001 | Deployment.default.privileged-demo-app |

## False positives (17)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-001-privileged-container-0001 | KSV-0001 | artifact.yaml |
| trivy-case-001-privileged-container-0002 | KSV-0003 | artifact.yaml |
| trivy-case-001-privileged-container-0003 | KSV-0004 | artifact.yaml |
| trivy-case-001-privileged-container-0004 | KSV-0011 | artifact.yaml |
| trivy-case-001-privileged-container-0005 | KSV-0012 | artifact.yaml |

Showing 5 of 17. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-001-privileged-container.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-001-privileged-container.metrics.json`
- Generated: `2026-09-17T06:59:44.178280+00:00`
