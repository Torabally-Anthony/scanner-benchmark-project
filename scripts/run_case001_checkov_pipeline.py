from pathlib import Path
import subprocess
import sys
import json
import shutil


CASE_ID = "case-001-privileged-container"

ARTIFACT_FILE = Path("corpus/kubernetes/case-001-privileged-container/artifact.yaml")

RAW_OUTPUT_DIR = Path("results/raw/checkov")
RAW_OUTPUT_FILE = RAW_OUTPUT_DIR / f"{CASE_ID}.json"
CHECKOV_VERSION_FILE = RAW_OUTPUT_DIR / "checkov-version.txt"


def run_python_script(script_path: str) -> None:
    print(f"\nRunning: {script_path}")

    result = subprocess.run(
        [sys.executable, script_path],
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Script failed: {script_path}")


def get_checkov_command() -> str:
    checkov_path = shutil.which("checkov")

    if checkov_path is None:
        raise RuntimeError(
            "Checkov was not found. Activate your virtual environment first:\n"
            ".\\.venv\\Scripts\\Activate.ps1"
        )

    print(f"Checkov found at: {checkov_path}")
    return checkov_path


def save_checkov_version(checkov_command: str) -> None:
    print("\nRecording Checkov version...")

    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [checkov_command, "--version"],
        text=True,
        capture_output=True,
        shell=True,
    )

    version_text = result.stdout.strip() or result.stderr.strip()

    if not version_text:
        raise RuntimeError("Could not read Checkov version.")

    CHECKOV_VERSION_FILE.write_text(version_text, encoding="utf-8")

    print(f"Checkov version saved to: {CHECKOV_VERSION_FILE}")
    print(f"Version: {version_text}")


def run_checkov_scan(checkov_command: str) -> None:
    print("\nRunning Checkov scan...")

    if not ARTIFACT_FILE.exists():
        raise FileNotFoundError(f"Artifact file not found: {ARTIFACT_FILE}")

    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    command = (
        f'"{checkov_command}" '
        f'--file "{ARTIFACT_FILE}" '
        f'--framework kubernetes '
        f'--output json'
    )

    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        shell=True,
    )

    # Checkov may return a non-zero exit code when it finds failed checks.
    # For this benchmark, failed checks are expected because the case is intentionally insecure.
    if result.stdout.strip():
        RAW_OUTPUT_FILE.write_text(result.stdout, encoding="utf-8")
    else:
        raise RuntimeError(
            "Checkov did not produce JSON output. Error output:\n"
            f"{result.stderr}"
        )

    # Validate that the raw output is actually JSON.
    try:
        json.loads(RAW_OUTPUT_FILE.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Checkov output was saved but is not valid JSON: {RAW_OUTPUT_FILE}\n"
            f"JSON error: {error}"
        )

    print(f"Raw Checkov output saved to: {RAW_OUTPUT_FILE}")

    if result.returncode != 0:
        print(
            "Checkov returned a non-zero exit code, but this is acceptable here "
            "because failed checks are expected in this benchmark case."
        )


def main():
    print("=" * 70)
    print("Running Case 001 Checkov End-to-End Benchmark Pipeline")
    print("=" * 70)

    checkov_command = get_checkov_command()

    run_python_script("scripts/validate_case.py")

    save_checkov_version(checkov_command)

    run_checkov_scan(checkov_command)

    run_python_script("scripts/normalize_checkov.py")

    run_python_script("scripts/match_checkov_to_ground_truth.py")

    run_python_script("scripts/compute_metrics_checkov.py")

    run_python_script("scripts/generate_case001_checkov_report.py")

    print("\n" + "=" * 70)
    print("Pipeline completed successfully.")
    print("=" * 70)

    print("\nGenerated outputs:")
    print(f"- Raw output: {RAW_OUTPUT_FILE}")
    print("- Normalised output: results/normalised/checkov/case-001-privileged-container.normalised.json")
    print("- Matched output: results/matched/checkov/case-001-privileged-container.matched.json")
    print("- Metrics output: results/metrics/checkov/case-001-privileged-container.metrics.json")
    print("- Report: results/reports/case-001-checkov-report.md")


if __name__ == "__main__":
    main()