# Benchmark Report: Trivy

**Case:** `case-docker-003-latest-base-image`

Artifact: `dockerfile` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 1 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 0 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 1 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 1 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-DOCKER-003 | UnpinnedBaseImage | Dockerfile | Detected | DS-0001 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-docker-003-latest-base-image-0001 | DS-0001 | GT-DOCKER-003 | Dockerfile |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_dockerfile/trivy/case-docker-003-latest-base-image.matched.json`
- Full metrics: `results/metrics_dockerfile/trivy/case-docker-003-latest-base-image.metrics.json`
- Generated: `2026-09-22T12:10:34.447827+00:00`
