# Benchmark Comparison Report

Generated: `2026-08-02T19:43:03.994255+00:00`

## Methodology note

Metrics are aggregated only across scanner–artifact combinations that are applicable.

Kubescape is marked **Not applicable** for Dockerfile cases and is not assigned false negatives for them.

In review mode, unlabelled extra findings are reported as review burden and are not automatically counted as false positives.

## Corpus overview

| Artifact family | Cases | Applicable scanners |
| --- | --- | --- |
| Kubernetes YAML | 2 | checkov, trivy, kubescape |
| Dockerfile | 2 | checkov, trivy |
| Helm chart | 2 | checkov, trivy, kubescape |

## Per-case results

| Case | Artifact | Scanner | TP | FP | FN | Extras | Precision | Recall | F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| case-001-privileged-container | Kubernetes YAML | checkov | 1 | 19 | 0 | 0 | 0.0500 | 1.0000 | 0.0952 |
| case-001-privileged-container | Kubernetes YAML | trivy | 1 | 17 | 0 | 0 | 0.0556 | 1.0000 | 0.1053 |
| case-001-privileged-container | Kubernetes YAML | kubescape | 1 | 22 | 0 | 0 | 0.0435 | 1.0000 | 0.0833 |
| case-002-runs-as-root | Kubernetes YAML | checkov | 1 | 4 | 0 | 0 | 0.2000 | 1.0000 | 0.3333 |
| case-002-runs-as-root | Kubernetes YAML | trivy | 1 | 3 | 0 | 0 | 0.2500 | 1.0000 | 0.4000 |
| case-002-runs-as-root | Kubernetes YAML | kubescape | 1 | 5 | 0 | 0 | 0.1667 | 1.0000 | 0.2857 |
| case-docker-001-root-user | Dockerfile | checkov | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-docker-001-root-user | Dockerfile | trivy | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-docker-002-missing-user | Dockerfile | checkov | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-docker-002-missing-user | Dockerfile | trivy | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-helm-001-host-network | Helm chart | checkov | 1 | 3 | 0 | 0 | 0.2500 | 1.0000 | 0.4000 |
| case-helm-001-host-network | Helm chart | trivy | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-helm-001-host-network | Helm chart | kubescape | 1 | 5 | 0 | 0 | 0.1667 | 1.0000 | 0.2857 |
| case-helm-002-host-pid | Helm chart | checkov | 1 | 3 | 0 | 0 | 0.2500 | 1.0000 | 0.4000 |
| case-helm-002-host-pid | Helm chart | trivy | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-helm-002-host-pid | Helm chart | kubescape | 1 | 6 | 0 | 0 | 0.1429 | 1.0000 | 0.2500 |

## Scanner coverage matrix

| Case | Artifact | Checkov | Trivy | Kubescape |
| --- | --- | --- | --- | --- |
| case-001-privileged-container | Kubernetes YAML | Detected | Detected | Detected |
| case-002-runs-as-root | Kubernetes YAML | Detected | Detected | Detected |
| case-docker-001-root-user | Dockerfile | Detected | Detected | Not applicable |
| case-docker-002-missing-user | Dockerfile | Detected | Detected | Not applicable |
| case-helm-001-host-network | Helm chart | Detected | Detected | Detected |
| case-helm-002-host-pid | Helm chart | Detected | Detected | Detected |

## Results by artifact family

### Kubernetes YAML

| Scanner | Cases | TP | FP | FN | Extras | Micro P | Micro R | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkov | 2 | 2 | 23 | 0 | 0 | 0.0800 | 1.0000 | 0.1481 | 0.2142 |
| trivy | 2 | 2 | 20 | 0 | 0 | 0.0909 | 1.0000 | 0.1667 | 0.2527 |
| kubescape | 2 | 2 | 27 | 0 | 0 | 0.0690 | 1.0000 | 0.1290 | 0.1845 |

### Dockerfile

| Scanner | Cases | TP | FP | FN | Extras | Micro P | Micro R | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkov | 2 | 2 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| trivy | 2 | 2 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

### Helm chart

| Scanner | Cases | TP | FP | FN | Extras | Micro P | Micro R | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkov | 2 | 2 | 6 | 0 | 0 | 0.2500 | 1.0000 | 0.4000 | 0.4000 |
| trivy | 2 | 2 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| kubescape | 2 | 2 | 11 | 0 | 0 | 0.1538 | 1.0000 | 0.2667 | 0.2679 |

## Overall scanner summary

| Scanner | Applicable cases | N/A cases | TP | FP | FN | Extras | Micro P | Micro R | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkov | 6 | 0 | 6 | 29 | 0 | 0 | 0.1714 | 1.0000 | 0.2927 | 0.5381 |
| trivy | 6 | 0 | 6 | 20 | 0 | 0 | 0.2308 | 1.0000 | 0.3750 | 0.7509 |
| kubescape | 4 | 2 | 4 | 38 | 0 | 0 | 0.0952 | 1.0000 | 0.1739 | 0.2262 |
