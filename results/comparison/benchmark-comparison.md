# Benchmark Comparison Report

Generated: `2026-09-17T07:07:17.379508+00:00`

Metrics include applicable scanner and artifact combinations only. Kubescape is not applicable to Dockerfile cases. Unmapped findings count as false positives.

## Corpus overview

| Artifact family | Cases | Applicable scanners |
| --- | --- | --- |
| Kubernetes YAML | 2 | checkov, trivy, kubescape |
| Dockerfile | 2 | checkov, trivy |
| Helm chart | 2 | checkov, trivy, kubescape |

## Per-case results

| Case | Scanner | TP | FP | FN | F1 |
| --- | --- | --- | --- | --- | --- |
| case-001-privileged-container | checkov | 1 | 19 | 0 | 0.0952 |
| case-001-privileged-container | trivy | 1 | 17 | 0 | 0.1053 |
| case-001-privileged-container | kubescape | 1 | 22 | 0 | 0.0833 |
| case-002-runs-as-root | checkov | 1 | 4 | 0 | 0.3333 |
| case-002-runs-as-root | trivy | 1 | 3 | 0 | 0.4000 |
| case-002-runs-as-root | kubescape | 1 | 5 | 0 | 0.2857 |
| case-docker-001-root-user | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-001-root-user | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-002-missing-user | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-002-missing-user | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-001-host-network | checkov | 1 | 3 | 0 | 0.4000 |
| case-helm-001-host-network | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-001-host-network | kubescape | 1 | 5 | 0 | 0.2857 |
| case-helm-002-host-pid | checkov | 1 | 3 | 0 | 0.4000 |
| case-helm-002-host-pid | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-002-host-pid | kubescape | 1 | 6 | 0 | 0.2500 |

## Overall scanner summary

| Scanner | Cases | TP | FP | FN | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- |
| checkov | 6 | 6 | 29 | 0 | 0.2927 | 0.5381 |
| trivy | 6 | 6 | 20 | 0 | 0.3750 | 0.7509 |
| kubescape | 4 | 4 | 38 | 0 | 0.1739 | 0.2262 |

Full breakdown: `results/comparison/benchmark-comparison.json`
