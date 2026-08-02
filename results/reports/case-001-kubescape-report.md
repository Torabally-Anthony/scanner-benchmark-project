# Case 001 Kubescape Benchmark Report

## 1. Case Summary

- Case ID: `case-001-privileged-container`
- Scanner: `kubescape`
- Artifact type: `kubernetes_yaml`
- Benchmark issue: Privileged container
- Ground truth ID: `GT-001`

## 2. Ground Truth Detection Result

- Ground truth items: `1`
- Normalised Kubescape findings: `23`
- Mapped findings: `1`
- Unmapped findings: `22`

## 3. True Positive Findings

- Ground truth: `GT-001`
  - Scanner rule: `C-0057`
  - Rule name: Privileged container
  - Resource: `Deployment.default.privileged-demo-app`
  - Container: `demo-container`
  - Field path: `spec.template.spec.containers[0].securityContext.privileged`
  - Evidence: Kubescape control C-0057 failed: Privileged container

## 4. False Negative Review

No false negatives were found. Kubescape detected the labelled ground-truth issue.

## 5. Metric Counts

- True positives: `1`
- False positives: `0`
- False negatives: `0`
- Unlabelled extra findings: `22`

## 6. Evaluation Metrics

- Precision: `1.0`
- Recall: `1.0`
- F1 score: `1.0`

## 7. Unlabelled Extra Findings

These findings were reported by Kubescape but are not counted as false positives yet because the benchmark is currently using review mode.

- `C-0004` — Resources memory limit and request (High)
- `C-0009` — Resource limits (High)
- `C-0013` — Non-root containers (Medium)
- `C-0016` — Allow privilege escalation (Medium)
- `C-0017` — Immutable container filesystem (Low)
- `C-0018` — Configured readiness probe (Low)
- `C-0030` — Ingress and Egress blocked (Medium)
- `C-0034` — Automatic mapping of service account (Medium)
- `C-0050` — Resources CPU limit and request (High)
- `C-0055` — Linux hardening (Medium)
- `C-0056` — Configured liveness probe (Medium)
- `C-0061` — Pods in default namespace (Low)
- `C-0077` — K8s common labels usage (Low)
- `C-0190` — Ensure that Service Account Tokens are only mounted where necessary (Medium)
- `C-0210` — Ensure that the seccomp profile is set to docker/default in your pod definitions (Medium)
- `C-0211` — Apply Security Context to Your Pods and Containers (High)
- `C-0237` — Check if signature exists (High)
- `C-0260` — Missing network policy (Medium)
- `C-0268` — Ensure CPU requests are set (Low)
- `C-0269` — Ensure memory requests are set (Low)
- `C-0270` — Ensure CPU limits are set (High)
- `C-0271` — Ensure memory limits are set (High)

## 8. Interpretation

Kubescape successfully detected the privileged container misconfiguration using control `C-0057`. This finding matched the ground truth label `GT-001`, so it was classified as a true positive.

The additional Kubescape failed controls were stored as unlabelled extras. They may represent valid security recommendations, but they are not part of the current ground-truth label set for this controlled benchmark case.

## 9. Conclusion

The first Kubescape benchmark run was successful. For case-001, Kubescape detected the intended privileged container issue, producing Precision = 1.0, Recall = 1.0, and F1 Score = 1.0 in review mode.
