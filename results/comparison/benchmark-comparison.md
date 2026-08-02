# Benchmark Comparison Report

Generated: `2026-08-02T17:44:47.161332+00:00`

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
| case-001-privileged-container | Kubernetes YAML | checkov | 1 | 0 | 0 | 19 | 1.0000 | 1.0000 | 1.0000 |
| case-001-privileged-container | Kubernetes YAML | trivy | 1 | 0 | 0 | 17 | 1.0000 | 1.0000 | 1.0000 |
| case-001-privileged-container | Kubernetes YAML | kubescape | 1 | 0 | 0 | 22 | 1.0000 | 1.0000 | 1.0000 |
| case-002-runs-as-root | Kubernetes YAML | checkov | 1 | 4 | 0 | 0 | 0.2000 | 1.0000 | 0.3333 |
| case-002-runs-as-root | Kubernetes YAML | trivy | 1 | 3 | 0 | 0 | 0.2500 | 1.0000 | 0.4000 |
| case-002-runs-as-root | Kubernetes YAML | kubescape | 1 | 5 | 0 | 0 | 0.1667 | 1.0000 | 0.2857 |
| case-docker-001-root-user | Dockerfile | checkov | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-docker-001-root-user | Dockerfile | trivy | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-docker-002-missing-user | Dockerfile | checkov | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-docker-002-missing-user | Dockerfile | trivy | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-helm-001-host-network | Helm chart | checkov | 1 | 0 | 0 | 3 | 1.0000 | 1.0000 | 1.0000 |
| case-helm-001-host-network | Helm chart | trivy | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-helm-001-host-network | Helm chart | kubescape | 1 | 0 | 0 | 5 | 1.0000 | 1.0000 | 1.0000 |
| case-helm-002-host-pid | Helm chart | checkov | 1 | 0 | 0 | 3 | 1.0000 | 1.0000 | 1.0000 |
| case-helm-002-host-pid | Helm chart | trivy | 1 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| case-helm-002-host-pid | Helm chart | kubescape | 1 | 0 | 0 | 6 | 1.0000 | 1.0000 | 1.0000 |

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
| checkov | 2 | 2 | 4 | 0 | 19 | 0.3333 | 1.0000 | 0.5000 | 0.6666 |
| trivy | 2 | 2 | 3 | 0 | 17 | 0.4000 | 1.0000 | 0.5714 | 0.7000 |
| kubescape | 2 | 2 | 5 | 0 | 22 | 0.2857 | 1.0000 | 0.4444 | 0.6429 |

### Dockerfile

| Scanner | Cases | TP | FP | FN | Extras | Micro P | Micro R | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkov | 2 | 2 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| trivy | 2 | 2 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

### Helm chart

| Scanner | Cases | TP | FP | FN | Extras | Micro P | Micro R | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkov | 2 | 2 | 0 | 0 | 6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| trivy | 2 | 2 | 0 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| kubescape | 2 | 2 | 0 | 0 | 11 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

## Overall scanner summary

| Scanner | Applicable cases | N/A cases | TP | FP | FN | Extras | Micro P | Micro R | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkov | 6 | 0 | 6 | 4 | 0 | 25 | 0.6000 | 1.0000 | 0.7500 | 0.8889 |
| trivy | 6 | 0 | 6 | 3 | 0 | 17 | 0.6667 | 1.0000 | 0.8000 | 0.9000 |
| kubescape | 4 | 2 | 4 | 5 | 0 | 33 | 0.4444 | 1.0000 | 0.6154 | 0.8214 |
