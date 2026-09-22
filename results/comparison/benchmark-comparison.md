# Benchmark Comparison Report

Generated: `2026-09-22T12:24:43.538871+00:00`

Metrics include applicable scanner and artifact combinations only. Kubescape is not applicable to Dockerfile cases. Unmapped findings count as false positives.

## Corpus overview

| Artifact family | Cases | Applicable scanners |
| --- | --- | --- |
| Kubernetes YAML | 10 | checkov, trivy, kubescape |
| Dockerfile | 10 | checkov, trivy |
| Helm chart | 10 | checkov, trivy, kubescape |

## Per-case results

| Case | Scanner | TP | FP | FN | F1 |
| --- | --- | --- | --- | --- | --- |
| case-001-privileged-container | checkov | 1 | 19 | 0 | 0.0952 |
| case-001-privileged-container | trivy | 1 | 17 | 0 | 0.1053 |
| case-001-privileged-container | kubescape | 1 | 22 | 0 | 0.0833 |
| case-002-runs-as-root | checkov | 1 | 4 | 0 | 0.3333 |
| case-002-runs-as-root | trivy | 1 | 3 | 0 | 0.4000 |
| case-002-runs-as-root | kubescape | 1 | 5 | 0 | 0.2857 |
| case-003-rbac-wildcard | checkov | 1 | 2 | 0 | 0.5000 |
| case-003-rbac-wildcard | trivy | 1 | 1 | 0 | 0.6667 |
| case-003-rbac-wildcard | kubescape | 0 | 0 | 1 | N/A |
| case-004-public-loadbalancer | checkov | 0 | 0 | 1 | N/A |
| case-004-public-loadbalancer | trivy | 0 | 0 | 1 | N/A |
| case-004-public-loadbalancer | kubescape | 0 | 1 | 1 | 0.0000 |
| case-005-hardcoded-secret | checkov | 0 | 0 | 1 | N/A |
| case-005-hardcoded-secret | trivy | 0 | 0 | 1 | N/A |
| case-005-hardcoded-secret | kubescape | 0 | 0 | 1 | N/A |
| case-006-latest-image-tag | checkov | 1 | 4 | 0 | 0.3333 |
| case-006-latest-image-tag | trivy | 1 | 2 | 0 | 0.5000 |
| case-006-latest-image-tag | kubescape | 0 | 9 | 1 | 0.0000 |
| case-007-missing-resource-limits | checkov | 1 | 7 | 0 | 0.2222 |
| case-007-missing-resource-limits | trivy | 1 | 4 | 0 | 0.3333 |
| case-007-missing-resource-limits | kubescape | 1 | 13 | 0 | 0.1333 |
| case-008-hostpath-volume | checkov | 0 | 5 | 1 | 0.0000 |
| case-008-hostpath-volume | trivy | 1 | 3 | 0 | 0.4000 |
| case-008-hostpath-volume | kubescape | 1 | 10 | 0 | 0.1667 |
| case-009-automount-service-account-token | checkov | 1 | 5 | 0 | 0.2857 |
| case-009-automount-service-account-token | trivy | 0 | 2 | 1 | 0.0000 |
| case-009-automount-service-account-token | kubescape | 1 | 9 | 0 | 0.1818 |
| case-010-dangerous-capability | checkov | 1 | 6 | 0 | 0.2500 |
| case-010-dangerous-capability | trivy | 1 | 4 | 0 | 0.3333 |
| case-010-dangerous-capability | kubescape | 1 | 10 | 0 | 0.1667 |
| case-docker-001-root-user | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-001-root-user | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-002-missing-user | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-002-missing-user | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-003-latest-base-image | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-003-latest-base-image | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-004-exposed-ssh-port | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-004-exposed-ssh-port | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-005-missing-healthcheck | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-005-missing-healthcheck | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-006-add-instead-of-copy | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-006-add-instead-of-copy | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-007-deprecated-maintainer | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-007-deprecated-maintainer | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-008-relative-workdir | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-008-relative-workdir | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-009-duplicate-stage-alias | checkov | 0 | 0 | 1 | N/A |
| case-docker-009-duplicate-stage-alias | trivy | 0 | 0 | 1 | N/A |
| case-docker-010-orphan-package-update | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-010-orphan-package-update | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-001-host-network | checkov | 1 | 3 | 0 | 0.4000 |
| case-helm-001-host-network | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-001-host-network | kubescape | 1 | 5 | 0 | 0.2857 |
| case-helm-002-host-pid | checkov | 1 | 3 | 0 | 0.4000 |
| case-helm-002-host-pid | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-002-host-pid | kubescape | 1 | 6 | 0 | 0.2500 |
| case-helm-003-privileged-container | checkov | 1 | 12 | 0 | 0.1429 |
| case-helm-003-privileged-container | trivy | 1 | 10 | 0 | 0.1667 |
| case-helm-003-privileged-container | kubescape | 1 | 20 | 0 | 0.0909 |
| case-helm-004-runs-as-root | checkov | 1 | 13 | 0 | 0.1333 |
| case-helm-004-runs-as-root | trivy | 1 | 12 | 0 | 0.1429 |
| case-helm-004-runs-as-root | kubescape | 1 | 19 | 0 | 0.0952 |
| case-helm-005-host-ipc | checkov | 1 | 12 | 0 | 0.1429 |
| case-helm-005-host-ipc | trivy | 1 | 10 | 0 | 0.1667 |
| case-helm-005-host-ipc | kubescape | 1 | 20 | 0 | 0.0909 |
| case-helm-006-hostpath-volume | checkov | 0 | 12 | 1 | 0.0000 |
| case-helm-006-hostpath-volume | trivy | 1 | 11 | 0 | 0.1538 |
| case-helm-006-hostpath-volume | kubescape | 1 | 21 | 0 | 0.0870 |
| case-helm-007-service-account-token | checkov | 1 | 12 | 0 | 0.1429 |
| case-helm-007-service-account-token | trivy | 0 | 10 | 1 | 0.0000 |
| case-helm-007-service-account-token | kubescape | 1 | 20 | 0 | 0.0909 |
| case-helm-008-dangerous-capability | checkov | 1 | 13 | 0 | 0.1333 |
| case-helm-008-dangerous-capability | trivy | 1 | 12 | 0 | 0.1429 |
| case-helm-008-dangerous-capability | kubescape | 1 | 21 | 0 | 0.0870 |
| case-helm-009-privilege-escalation | checkov | 1 | 12 | 0 | 0.1429 |
| case-helm-009-privilege-escalation | trivy | 1 | 10 | 0 | 0.1667 |
| case-helm-009-privilege-escalation | kubescape | 1 | 20 | 0 | 0.0909 |
| case-helm-010-public-loadbalancer | checkov | 0 | 1 | 1 | 0.0000 |
| case-helm-010-public-loadbalancer | trivy | 0 | 0 | 1 | N/A |
| case-helm-010-public-loadbalancer | kubescape | 0 | 1 | 1 | 0.0000 |

## Overall scanner summary

| Scanner | Cases | TP | FP | FN | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- |
| checkov | 30 | 24 | 145 | 6 | 24.12% | 46.88% |
| trivy | 30 | 24 | 111 | 6 | 29.09% | 56.45% |
| kubescape | 20 | 15 | 232 | 5 | 11.24% | 12.14% |

Full breakdown: `results/comparison/benchmark-comparison.json`
