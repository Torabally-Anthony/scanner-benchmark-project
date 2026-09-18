# Benchmark Report: Checkov

**Case:** `case-docker-002-missing-user`

Artifact: `dockerfile` · Mode: `strict` · Status: `complete`

Scanner version: `2.5.20`

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
| GT-DOCKER-002 | MissingUserInstruction | Dockerfile.default.Dockerfile | Detected | CKV_DOCKER_3 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-docker-002-missing-user-0001 | CKV_DOCKER_3 | GT-DOCKER-002 | Dockerfile.default.Dockerfile |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_dockerfile/checkov/case-docker-002-missing-user.matched.json`
- Full metrics: `results/metrics_dockerfile/checkov/case-docker-002-missing-user.metrics.json`
- Generated: `2026-09-17T06:59:44.352934+00:00`
