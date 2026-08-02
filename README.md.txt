# Security Scanner Benchmark Project

This project compares infrastructure-as-code security scanners against a controlled ground truth. It currently evaluates **Checkov**, **Trivy**, and **Kubescape** across Kubernetes YAML, Dockerfiles, and Helm charts.

Each benchmark case contains an intentionally insecure artifact and a `ground_truth.yaml` file describing the expected finding. Scanner results are converted into a common format, matched to the ground truth, scored, and rendered as Markdown reports.

## Benchmark workflow

```text
Benchmark artifact + ground truth
              |
              v
      Run applicable scanner
              |
              v
       Raw scanner JSON
              |
              v
          Normalise
              |
              v
    Match to ground truth
              |
              v
 Calculate precision/recall/F1
              |
              v
   JSON and Markdown reports
```

The pipeline scripts process **existing raw scanner JSON files**. They do not launch Checkov, Trivy, or Kubescape. Run the scanner first and save its JSON output under `results/raw/<scanner>/`.

## Supported scanners and artifacts

| Artifact | Checkov | Trivy | Kubescape |
| --- | --- | --- | --- |
| Kubernetes YAML | Yes | Yes | Yes |
| Dockerfile | Yes | Yes | Not applicable |
| Helm chart | Yes | Yes | Yes |

Kubescape is not evaluated against Dockerfiles and is not assigned false negatives for those cases.

## Configured benchmark cases

The case registry and scanner rule mappings are defined in `config/benchmark_config.yaml`.

| Case | Artifact | Intended issue |
| --- | --- | --- |
| `case-001-privileged-container` | Kubernetes YAML | Privileged container |
| `case-002-runs-as-root` | Kubernetes YAML | Container runs as root |
| `case-docker-001-root-user` | Dockerfile | Root user configured |
| `case-docker-002-missing-user` | Dockerfile | Missing non-root `USER` instruction |
| `case-helm-001-host-network` | Helm chart | Host network enabled |
| `case-helm-002-host-pid` | Helm chart | Host PID enabled |

## Repository structure

```text
scanner-benchmark-project/
|-- backend/                 FastAPI backend
|-- config/                  Case registry and rule mappings
|-- corpus/
|   |-- kubernetes/          Kubernetes YAML cases
|   |-- dockerfiles/         Dockerfile cases
|   `-- helm/                Helm chart cases
|-- frontend/                Dashboard HTML, CSS, and JavaScript
|-- scripts/                 Validation and benchmark pipeline scripts
|-- tools/                   Local scanner directories and documentation
`-- results/
    |-- raw/                 Original scanner JSON
    |-- normalised_generic/  Normalised Kubernetes findings
    |-- matched_generic/     Kubernetes ground-truth matches
    |-- metrics_generic/     Kubernetes metrics
    |-- reports_generic/     Kubernetes reports
    |-- normalised_dockerfile/
    |-- matched_dockerfile/
    |-- metrics_dockerfile/
    |-- reports_dockerfile/
    |-- normalised_helm/
    |-- matched_helm/
    |-- metrics_helm/
    |-- reports_helm/
    `-- comparison/          Combined JSON and Markdown comparison
```

## Requirements

- Python 3.10 or newer
- Checkov
- Trivy
- Kubescape for Kubernetes and Helm cases
- A web browser for the dashboard

The scanner executables are intentionally excluded from Git because the Trivy and Kubescape binaries exceed GitHub's normal file-size limit. Install or download them locally after cloning.

## Python setup

From the project root on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pyyaml fastapi uvicorn pydantic checkov
```

Trivy and Kubescape are separate command-line applications. Place local copies at these paths if you want to use the same commands shown below:

```text
tools/trivy/trivy.exe
tools/kubescape/kubescape.exe
```

Confirm the tools are available:

```powershell
checkov --version
.\tools\trivy\trivy.exe --version
.\tools\kubescape\kubescape.exe version
```

## Raw scanner results

Every pipeline expects this naming convention:

```text
results/raw/<scanner>/<case-id>.json
```

For example, generate the Trivy input for the first Kubernetes case with:

```powershell
New-Item -ItemType Directory -Force results/raw/trivy | Out-Null

.\tools\trivy\trivy.exe config `
  --format json `
  --output results/raw/trivy/case-001-privileged-container.json `
  corpus/kubernetes/case-001-privileged-container/artifact.yaml
```

The processing pipeline will fail its preflight check if the expected raw JSON file is missing, empty, or invalid.

## Validate the configuration and cases

Validate the complete benchmark configuration:

```powershell
python scripts/validate_benchmark_config.py
```

Run the legacy validation for `case-001-privileged-container`:

```powershell
python scripts/validate_case.py
```

`validate_case.py` is currently hard-coded to the first Kubernetes case. The configuration validator also expects a mapping entry for every default scanner; because Kubescape is intentionally not applicable to Dockerfiles, the current Dockerfile configuration may be reported as missing a Kubescape mapping even though the Dockerfile runner correctly supports only Checkov and Trivy.

## Run the benchmark pipelines

These commands assume the required raw scanner JSON files already exist.

### Kubernetes YAML

Process all configured scanners:

```powershell
python scripts/run_benchmark.py --case case-001-privileged-container
```

Process only selected scanners:

```powershell
python scripts/run_benchmark.py `
  --case case-001-privileged-container `
  --scanners checkov trivy kubescape
```

### Dockerfile

```powershell
python scripts/run_dockerfile_benchmark.py `
  --case case-docker-001-root-user `
  --scanners checkov trivy
```

### Helm chart

```powershell
python scripts/run_helm_benchmark.py `
  --case case-helm-001-host-network `
  --scanners checkov trivy kubescape
```

Add `--continue-on-error` to continue processing the remaining scanners when one scanner fails.

## Matching modes

The default matching mode is `review` and is configured in `config/benchmark_config.yaml`.

- `review`: unmapped scanner findings are recorded as unlabelled extras and are not automatically counted as false positives.
- `strict`: unmapped findings are counted as false positives.

Choose a mode on the command line:

```powershell
python scripts/run_benchmark.py `
  --case case-001-privileged-container `
  --scanners trivy `
  --matching-mode strict
```

## Pipeline stages

The artifact-specific runners call four generic scripts in order:

1. `normalize_findings.py` converts scanner-specific JSON into the common benchmark schema.
2. `match_findings.py` compares normalised findings with the case ground truth and configured rule mappings.
3. `compute_metrics.py` calculates true positives, false positives, false negatives, precision, recall, and F1 score.
4. `generate_report.py` creates a readable Markdown report.

The main metric formulas are:

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 * Precision * Recall / (Precision + Recall)
```

## Generate the combined comparison

After all required case metrics have been generated, run:

```powershell
python scripts/generate_comparison_report.py
```

This creates:

```text
results/comparison/benchmark-comparison.json
results/comparison/benchmark-comparison.md
```

The comparison contains per-case results, scanner coverage, artifact-family summaries, and overall micro and macro metrics.

## Run the dashboard

The FastAPI application serves both the API and the frontend:

```powershell
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The dashboard can:

- list configured benchmark cases;
- validate case files;
- process existing raw outputs;
- display scanner metrics and intermediate JSON;
- generate and open comparison reports.

The dashboard's Run/Process action does **not** execute scanner CLI tools. If a scanner reports that its raw output is missing, generate the expected file under `results/raw/<scanner>/` first.

## Result classifications

- **True positive (TP):** the scanner finding matches a labelled ground-truth issue.
- **False positive (FP):** a reported finding counted as incorrect under the selected matching mode.
- **False negative (FN):** a labelled ground-truth issue that the scanner did not detect.
- **Unlabelled extra:** a scanner finding without a configured ground-truth mapping; retained for review in review mode.
- **Duplicate match:** more than one finding matches the same ground-truth issue.
- **Ambiguous match:** a finding cannot be assigned confidently to exactly one ground-truth item.

## Troubleshooting

### Raw scanner output does not exist

Example:

```text
Raw trivy output does not exist:
results/raw/trivy/case-001-privileged-container.json
```

Run the scanner and save its JSON using the required case ID and directory, then rerun the processing pipeline.

### Trivy or Kubescape executable is missing

The binaries are not stored in Git. Download them locally or install them through your preferred package manager. Confirm their paths with the version commands in the setup section.

### Port already in use

If port 5500 is occupied, run the application on port 8000 as shown above. You may choose another free port if necessary.

### Comparison generation fails

The comparison generator expects metrics for every selected applicable scanner-case combination. Run the relevant artifact-specific pipelines before generating the comparison, or limit the comparison to cases whose metrics exist:

```powershell
python scripts/generate_comparison_report.py `
  --cases case-001-privileged-container
```

## Adding a benchmark case

1. Add the insecure artifact to the appropriate folder under `corpus/`.
2. Add a matching `ground_truth.yaml` file.
3. Register the case in `config/benchmark_config.yaml`.
4. Add scanner rule IDs under the case's `rule_mappings`.
5. Generate raw scanner JSON using the exact case ID.
6. Run the appropriate artifact-specific pipeline.
7. Review the normalised findings, matches, metrics, and report.
8. Regenerate the combined comparison report.

## Security note

The corpus is intentionally insecure and exists only for controlled static-analysis benchmarking. Do not deploy these manifests, Dockerfiles, or Helm charts to production systems.
