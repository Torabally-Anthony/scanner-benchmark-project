# Benchmark Comparison Report

Generated: `2026-10-21T11:14:52.290991+00:00`

Metrics include applicable scanner and artifact combinations only. Kubescape is not applicable to Dockerfile cases. Unmapped findings count as false positives.

## Corpus overview

| Artifact family | Cases | Applicable scanners |
| --- | --- | --- |
| Kubernetes YAML | 20 | checkov, trivy, kubescape |
| Dockerfile | 20 | checkov, trivy |
| Helm chart | 20 | checkov, trivy, kubescape |

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
| case-011-host-network | checkov | 1 | 1 | 0 | 0.6667 |
| case-011-host-network | trivy | 1 | 0 | 0 | 1.0000 |
| case-011-host-network | kubescape | 1 | 4 | 0 | 0.3333 |
| case-012-host-pid | checkov | 1 | 1 | 0 | 0.6667 |
| case-012-host-pid | trivy | 1 | 0 | 0 | 1.0000 |
| case-012-host-pid | kubescape | 1 | 4 | 0 | 0.3333 |
| case-013-host-ipc | checkov | 1 | 1 | 0 | 0.6667 |
| case-013-host-ipc | trivy | 1 | 0 | 0 | 1.0000 |
| case-013-host-ipc | kubescape | 1 | 4 | 0 | 0.3333 |
| case-014-privilege-escalation | checkov | 1 | 1 | 0 | 0.6667 |
| case-014-privilege-escalation | trivy | 1 | 0 | 0 | 1.0000 |
| case-014-privilege-escalation | kubescape | 1 | 4 | 0 | 0.3333 |
| case-015-writable-root-filesystem | checkov | 1 | 1 | 0 | 0.6667 |
| case-015-writable-root-filesystem | trivy | 1 | 0 | 0 | 1.0000 |
| case-015-writable-root-filesystem | kubescape | 1 | 4 | 0 | 0.3333 |
| case-016-missing-liveness-probe | checkov | 1 | 1 | 0 | 0.6667 |
| case-016-missing-liveness-probe | trivy | 0 | 0 | 1 | N/A |
| case-016-missing-liveness-probe | kubescape | 1 | 4 | 0 | 0.3333 |
| case-017-missing-readiness-probe | checkov | 1 | 1 | 0 | 0.6667 |
| case-017-missing-readiness-probe | trivy | 0 | 0 | 1 | N/A |
| case-017-missing-readiness-probe | kubescape | 1 | 4 | 0 | 0.3333 |
| case-018-default-namespace | checkov | 1 | 1 | 0 | 0.6667 |
| case-018-default-namespace | trivy | 1 | 0 | 0 | 1.0000 |
| case-018-default-namespace | kubescape | 1 | 4 | 0 | 0.3333 |
| case-019-unconfined-seccomp | checkov | 1 | 1 | 0 | 0.6667 |
| case-019-unconfined-seccomp | trivy | 1 | 0 | 0 | 1.0000 |
| case-019-unconfined-seccomp | kubescape | 1 | 4 | 0 | 0.3333 |
| case-020-missing-network-policy | checkov | 0 | 1 | 1 | 0.0000 |
| case-020-missing-network-policy | trivy | 0 | 0 | 1 | N/A |
| case-020-missing-network-policy | kubescape | 1 | 4 | 0 | 0.3333 |
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
| case-docker-011-apt-command | checkov | 1 | 0 | 0 | 1.0000 |
| case-docker-011-apt-command | trivy | 0 | 0 | 1 | N/A |
| case-docker-012-multiple-entrypoints | checkov | 0 | 0 | 1 | N/A |
| case-docker-012-multiple-entrypoints | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-013-out-of-range-port | checkov | 0 | 0 | 1 | N/A |
| case-docker-013-out-of-range-port | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-014-sudo-in-run | checkov | 0 | 0 | 1 | N/A |
| case-docker-014-sudo-in-run | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-015-copy-destination-no-slash | checkov | 0 | 0 | 1 | N/A |
| case-docker-015-copy-destination-no-slash | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-016-run-cd-instead-of-workdir | checkov | 0 | 0 | 1 | N/A |
| case-docker-016-run-cd-instead-of-workdir | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-017-mixed-curl-wget | checkov | 0 | 0 | 1 | N/A |
| case-docker-017-mixed-curl-wget | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-018-yum-cache-not-cleaned | checkov | 0 | 0 | 1 | N/A |
| case-docker-018-yum-cache-not-cleaned | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-019-multiple-cmd | checkov | 0 | 0 | 1 | N/A |
| case-docker-019-multiple-cmd | trivy | 1 | 0 | 0 | 1.0000 |
| case-docker-020-apk-cache-not-disabled | checkov | 0 | 0 | 1 | N/A |
| case-docker-020-apk-cache-not-disabled | trivy | 1 | 0 | 0 | 1.0000 |
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
| case-helm-011-rbac-wildcard | checkov | 1 | 2 | 0 | 0.5000 |
| case-helm-011-rbac-wildcard | trivy | 1 | 1 | 0 | 0.6667 |
| case-helm-011-rbac-wildcard | kubescape | 0 | 0 | 1 | N/A |
| case-helm-012-latest-image-tag | checkov | 1 | 1 | 0 | 0.6667 |
| case-helm-012-latest-image-tag | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-012-latest-image-tag | kubescape | 0 | 3 | 1 | 0.0000 |
| case-helm-013-missing-resource-limits | checkov | 1 | 1 | 0 | 0.6667 |
| case-helm-013-missing-resource-limits | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-013-missing-resource-limits | kubescape | 1 | 3 | 0 | 0.4000 |
| case-helm-014-writable-root-filesystem | checkov | 1 | 1 | 0 | 0.6667 |
| case-helm-014-writable-root-filesystem | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-014-writable-root-filesystem | kubescape | 1 | 3 | 0 | 0.4000 |
| case-helm-015-missing-liveness-probe | checkov | 1 | 1 | 0 | 0.6667 |
| case-helm-015-missing-liveness-probe | trivy | 0 | 0 | 1 | N/A |
| case-helm-015-missing-liveness-probe | kubescape | 1 | 3 | 0 | 0.4000 |
| case-helm-016-missing-readiness-probe | checkov | 1 | 1 | 0 | 0.6667 |
| case-helm-016-missing-readiness-probe | trivy | 0 | 0 | 1 | N/A |
| case-helm-016-missing-readiness-probe | kubescape | 1 | 3 | 0 | 0.4000 |
| case-helm-017-default-namespace | checkov | 1 | 1 | 0 | 0.6667 |
| case-helm-017-default-namespace | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-017-default-namespace | kubescape | 1 | 3 | 0 | 0.4000 |
| case-helm-018-unconfined-seccomp | checkov | 1 | 1 | 0 | 0.6667 |
| case-helm-018-unconfined-seccomp | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-018-unconfined-seccomp | kubescape | 1 | 3 | 0 | 0.4000 |
| case-helm-019-missing-network-policy | checkov | 0 | 1 | 1 | 0.0000 |
| case-helm-019-missing-network-policy | trivy | 0 | 0 | 1 | N/A |
| case-helm-019-missing-network-policy | kubescape | 1 | 3 | 0 | 0.4000 |
| case-helm-020-host-port | checkov | 1 | 1 | 0 | 0.6667 |
| case-helm-020-host-port | trivy | 1 | 0 | 0 | 1.0000 |
| case-helm-020-host-port | kubescape | 1 | 3 | 0 | 0.4000 |

## Overall scanner summary

| Scanner | Cases | TP | FP | FN | Micro F1 | Macro F1 |
| --- | --- | --- | --- | --- | --- | --- |
| checkov | 60 | 43 | 166 | 17 | 31.97% | 53.11% |
| trivy | 60 | 47 | 112 | 13 | 42.92% | 76.21% |
| kubescape | 40 | 33 | 299 | 7 | 17.74% | 23.56% |

Full breakdown: `results/comparison/benchmark-comparison.json`
