# Benchmark Report: Trivy

**Case:** `case-helm-008-dangerous-capability`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 13 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 12 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0769 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.1429 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-008 | DangerousCapability | Deployment.default.capability-helm-demo | Detected | KSV-0005 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-helm-008-dangerous-capability-0001 | KSV-0005 | GT-HELM-008 | Deployment.default.capability-helm-demo |

## False positives (12)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-helm-008-dangerous-capability-0002 | KSV-0011 | templates/deployment.yaml |
| trivy-case-helm-008-dangerous-capability-0003 | KSV-0014 | templates/deployment.yaml |
| trivy-case-helm-008-dangerous-capability-0004 | KSV-0015 | templates/deployment.yaml |
| trivy-case-helm-008-dangerous-capability-0005 | KSV-0016 | templates/deployment.yaml |
| trivy-case-helm-008-dangerous-capability-0006 | KSV-0018 | templates/deployment.yaml |

Showing 5 of 12. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/trivy/case-helm-008-dangerous-capability.matched.json`
- Full metrics: `results/metrics_helm/trivy/case-helm-008-dangerous-capability.metrics.json`
- Generated: `2026-09-22T12:10:57.835824+00:00`
