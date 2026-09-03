from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from config_loader import (
    CONFIG_PATH,
    PROJECT_ROOT,
    ConfigurationError,
    get_ground_truth_items,
    load_benchmark_config,
    load_case_ground_truth,
)


SUPPORTED_SCANNERS = {
    "checkov",
    "trivy",
    "kubescape",
}

SUPPORTED_MATCHING_MODES = {
    "review",
    "strict",
}


class ConfigurationValidationError(Exception):
    """Raised when benchmark configuration validation fails."""


# This function returns a stripped string or None.
def clean_text(
    value: Any,
) -> str | None:
    """Return a stripped string or None."""

    if not isinstance(value, str):
        return None

    cleaned_value = value.strip()

    return cleaned_value or None


# This function resolves a configuration path and confirms that it remains inside the benchmark project.
def resolve_project_path(
    path_value: Any,
    field_name: str,
) -> Path:
    """
    Resolve a configuration path and confirm that it remains
    inside the benchmark project.
    """

    clean_path = clean_text(path_value)

    if clean_path is None:
        raise ConfigurationValidationError(
            f"{field_name} must be a non-empty string."
        )

    resolved_path = (
        PROJECT_ROOT / clean_path
    ).resolve()

    # Reject path traversal so configuration cannot reference files outside the project.
    try:
        resolved_path.relative_to(
            PROJECT_ROOT.resolve()
        )

    except ValueError as error:
        raise ConfigurationValidationError(
            f"{field_name} must point to a location "
            "inside the benchmark project."
        ) from error

    return resolved_path


# This function returns a readable project-relative path.
def display_project_path(
    path: Path,
) -> str:
    """Return a readable project-relative path."""

    try:
        return str(
            path.relative_to(PROJECT_ROOT)
        )

    except ValueError:
        return str(path)


# This function validates the configuration schema version.
def validate_schema_version(
    configuration: dict[str, Any],
) -> str:
    """Validate the configuration schema version."""

    schema_version = clean_text(
        configuration.get("schema_version")
    )

    if schema_version is None:
        raise ConfigurationValidationError(
            "schema_version is missing or invalid."
        )

    if schema_version != "1.0":
        raise ConfigurationValidationError(
            "Unsupported schema version "
            f"'{schema_version}'. Expected '1.0'."
        )

    print(
        f"[OK] Schema version: {schema_version}"
    )

    return schema_version


# This function validates default matching mode and scanner list.
def validate_defaults(
    configuration: dict[str, Any],
) -> tuple[str, list[str]]:
    """Validate default matching mode and scanner list."""

    defaults = configuration.get(
        "defaults",
        {},
    )

    if not isinstance(defaults, dict):
        raise ConfigurationValidationError(
            "defaults must be a YAML object."
        )

    matching_mode = clean_text(
        defaults.get("matching_mode")
    )

    if matching_mode is None:
        raise ConfigurationValidationError(
            "defaults.matching_mode is missing."
        )

    matching_mode = matching_mode.lower()

    if matching_mode not in SUPPORTED_MATCHING_MODES:
        raise ConfigurationValidationError(
            "defaults.matching_mode must be "
            "'review' or 'strict'."
        )

    print(
        f"[OK] Default matching mode: "
        f"{matching_mode}"
    )

    configured_scanners = defaults.get(
        "scanners"
    )

    if not isinstance(
        configured_scanners,
        list,
    ):
        raise ConfigurationValidationError(
            "defaults.scanners must be a list."
        )

    scanners: list[str] = []
    seen_scanners: set[str] = set()

    for index, scanner_value in enumerate(
        configured_scanners,
        start=1,
    ):
        scanner = clean_text(scanner_value)

        if scanner is None:
            raise ConfigurationValidationError(
                "defaults.scanners contains an invalid "
                f"value at position {index}."
            )

        scanner = scanner.lower()

        if scanner not in SUPPORTED_SCANNERS:
            supported = ", ".join(
                sorted(SUPPORTED_SCANNERS)
            )

            raise ConfigurationValidationError(
                f"Unsupported scanner '{scanner}' in "
                "defaults.scanners. Supported scanners: "
                f"{supported}."
            )

        if scanner in seen_scanners:
            raise ConfigurationValidationError(
                f"Scanner '{scanner}' appears more than "
                "once in defaults.scanners."
            )

        seen_scanners.add(scanner)
        scanners.append(scanner)

    if not scanners:
        raise ConfigurationValidationError(
            "defaults.scanners must contain at least "
            "one scanner."
        )

    print(
        "[OK] Default scanners: "
        + ", ".join(scanners)
    )

    return matching_mode, scanners


# This function validates the optional shared path configuration.
def validate_optional_paths(
    configuration: dict[str, Any],
) -> None:
    """Validate the optional shared path configuration."""

    paths = configuration.get(
        "paths",
        {},
    )

    if paths is None:
        return

    if not isinstance(paths, dict):
        raise ConfigurationValidationError(
            "paths must be a YAML object."
        )

    supported_path_fields = {
        "corpus_root",
        "results_root",
        "reports_root",
    }

    for field_name, path_value in paths.items():
        if field_name not in supported_path_fields:
            print(
                f"[WARNING] Unknown paths field: "
                f"{field_name}"
            )
            continue

        resolved_path = resolve_project_path(
            path_value,
            f"paths.{field_name}",
        )

        print(
            f"[OK] Path {field_name}: "
            f"{display_project_path(resolved_path)}"
        )


# This function validates one scanner's rule-ID list.
def validate_rule_id_list(
    case_id: str,
    ground_truth_id: str,
    scanner: str,
    rule_ids: Any,
) -> list[str]:
    """
    Validate one scanner's rule-ID list.

    Empty lists are allowed during the rule-discovery stage.
    """

    if not isinstance(rule_ids, list):
        raise ConfigurationValidationError(
            f"Case '{case_id}', ground-truth ID "
            f"'{ground_truth_id}', scanner '{scanner}' "
            "must use a list of rule IDs."
        )

    cleaned_rule_ids: list[str] = []
    seen_rule_ids: set[str] = set()

    for index, rule_id_value in enumerate(
        rule_ids,
        start=1,
    ):
        rule_id = clean_text(
            rule_id_value
        )

        if rule_id is None:
            raise ConfigurationValidationError(
                f"Case '{case_id}', ground-truth ID "
                f"'{ground_truth_id}', scanner "
                f"'{scanner}' contains an invalid rule "
                f"ID at position {index}."
            )

        normalised_rule_id = (
            rule_id.upper()
        )

        if normalised_rule_id in seen_rule_ids:
            raise ConfigurationValidationError(
                f"Duplicate rule ID '{rule_id}' for "
                f"scanner '{scanner}' under "
                f"ground-truth ID '{ground_truth_id}'."
            )

        seen_rule_ids.add(
            normalised_rule_id
        )

        cleaned_rule_ids.append(
            rule_id
        )

    return cleaned_rule_ids


# This function validates the artifact and ground-truth paths.
def validate_case_paths(
    case_id: str,
    case_configuration: dict[str, Any],
) -> tuple[Path, Path]:
    """Validate the artifact and ground-truth paths."""

    artifact_path = resolve_project_path(
        case_configuration.get(
            "artifact_path"
        ),
        (
            f"cases.{case_id}."
            "artifact_path"
        ),
    )

    ground_truth_path = resolve_project_path(
        case_configuration.get(
            "ground_truth_path"
        ),
        (
            f"cases.{case_id}."
            "ground_truth_path"
        ),
    )

    if not artifact_path.exists():
        raise ConfigurationValidationError(
            f"Artifact file does not exist: "
            f"{display_project_path(artifact_path)}"
        )

    if not artifact_path.is_file():
        raise ConfigurationValidationError(
            f"Artifact path is not a file: "
            f"{display_project_path(artifact_path)}"
        )

    if not ground_truth_path.exists():
        raise ConfigurationValidationError(
            f"Ground-truth file does not exist: "
            f"{display_project_path(ground_truth_path)}"
        )

    if not ground_truth_path.is_file():
        raise ConfigurationValidationError(
            f"Ground-truth path is not a file: "
            f"{display_project_path(ground_truth_path)}"
        )

    print(
        "  [OK] Artifact: "
        f"{display_project_path(artifact_path)}"
    )

    print(
        "  [OK] Ground truth: "
        f"{display_project_path(ground_truth_path)}"
    )

    return artifact_path, ground_truth_path


# This function confirms the configured artifact types agree.
def validate_artifact_type(
    case_id: str,
    case_configuration: dict[str, Any],
    ground_truth: dict[str, Any],
) -> None:
    """Confirm the configured artifact types agree."""

    configured_artifact_type = clean_text(
        case_configuration.get(
            "artifact_type"
        )
    )

    ground_truth_artifact_type = clean_text(
        ground_truth.get(
            "artifact_type"
        )
    )

    if configured_artifact_type is None:
        raise ConfigurationValidationError(
            f"Case '{case_id}' has no valid "
            "artifact_type."
        )

    if ground_truth_artifact_type is None:
        raise ConfigurationValidationError(
            f"Ground truth for case '{case_id}' "
            "has no valid artifact_type."
        )

    if (
        configured_artifact_type
        != ground_truth_artifact_type
    ):
        raise ConfigurationValidationError(
            f"Artifact type mismatch for case "
            f"'{case_id}'. Configuration contains "
            f"'{configured_artifact_type}', while "
            "ground truth contains "
            f"'{ground_truth_artifact_type}'."
        )

    print(
        "  [OK] Artifact type: "
        f"{configured_artifact_type}"
    )


# This function confirms the ground-truth case ID matches its config key.
def validate_case_id_match(
    configured_case_id: str,
    ground_truth: dict[str, Any],
) -> None:
    """Confirm the ground-truth case ID matches its config key."""

    ground_truth_case_id = clean_text(
        ground_truth.get("case_id")
    )

    if ground_truth_case_id is None:
        raise ConfigurationValidationError(
            f"Ground truth for '{configured_case_id}' "
            "has no valid case_id."
        )

    if ground_truth_case_id != configured_case_id:
        raise ConfigurationValidationError(
            "Case ID mismatch. Configuration key is "
            f"'{configured_case_id}', but ground truth "
            f"contains '{ground_truth_case_id}'."
        )

    print("  [OK] Case IDs match")


# This function validates mappings between ground-truth IDs and scanner rules.
def validate_rule_mappings(
    case_id: str,
    case_configuration: dict[str, Any],
    ground_truth_items: dict[str, dict[str, Any]],
    configured_scanners: list[str],
) -> int:
    """
    Validate mappings between ground-truth IDs and scanner rules.

    Returns the number of warnings generated.
    """

    rule_mappings = case_configuration.get(
        "rule_mappings"
    )

    if not isinstance(rule_mappings, dict):
        raise ConfigurationValidationError(
            f"Case '{case_id}' must contain a "
            "rule_mappings object."
        )

    ground_truth_ids = set(
        ground_truth_items.keys()
    )

    mapping_ground_truth_ids = set(
        str(value)
        for value in rule_mappings.keys()
    )

    unknown_mapping_ids = (
        mapping_ground_truth_ids
        - ground_truth_ids
    )

    if unknown_mapping_ids:
        raise ConfigurationValidationError(
            f"Case '{case_id}' has mappings for "
            "unknown ground-truth IDs: "
            + ", ".join(
                sorted(
                    unknown_mapping_ids
                )
            )
        )

    missing_mapping_ids = (
        ground_truth_ids
        - mapping_ground_truth_ids
    )

    if missing_mapping_ids:
        raise ConfigurationValidationError(
            f"Case '{case_id}' has no rule mappings "
            "for ground-truth IDs: "
            + ", ".join(
                sorted(
                    missing_mapping_ids
                )
            )
        )

    warning_count = 0

    for ground_truth_id in sorted(
        ground_truth_ids
    ):
        scanner_mappings = (
            rule_mappings.get(
                ground_truth_id
            )
        )

        if not isinstance(
            scanner_mappings,
            dict,
        ):
            raise ConfigurationValidationError(
                f"Rule mapping for "
                f"'{ground_truth_id}' in case "
                f"'{case_id}' must be a YAML object."
            )

        unknown_scanners = (
            set(scanner_mappings.keys())
            - SUPPORTED_SCANNERS
        )

        if unknown_scanners:
            raise ConfigurationValidationError(
                f"Ground-truth ID "
                f"'{ground_truth_id}' contains "
                "unsupported scanners: "
                + ", ".join(
                    sorted(
                        str(scanner)
                        for scanner
                        in unknown_scanners
                    )
                )
            )

        for scanner in configured_scanners:
            if scanner not in scanner_mappings:
                raise ConfigurationValidationError(
                    f"Ground-truth ID "
                    f"'{ground_truth_id}' has no "
                    f"mapping entry for scanner "
                    f"'{scanner}'. Use an empty list "
                    "during rule discovery."
                )

            cleaned_rule_ids = (
                validate_rule_id_list(
                    case_id=case_id,
                    ground_truth_id=(
                        ground_truth_id
                    ),
                    scanner=scanner,
                    rule_ids=(
                        scanner_mappings[
                            scanner
                        ]
                    ),
                )
            )

            if not cleaned_rule_ids:
                warning_count += 1

                print(
                    f"  [WARNING] "
                    f"{ground_truth_id} -> "
                    f"{scanner}: no rule IDs "
                    "configured yet"
                )

                continue

            print(
                f"  [OK] {ground_truth_id} -> "
                f"{scanner}: "
                f"{', '.join(cleaned_rule_ids)}"
            )

    return warning_count


# This function validates one benchmark case.
def validate_case(
    case_id: str,
    case_configuration: Any,
    configured_scanners: list[str],
) -> int:
    """Validate one benchmark case."""

    if not isinstance(
        case_configuration,
        dict,
    ):
        raise ConfigurationValidationError(
            f"Configuration for case '{case_id}' "
            "must be a YAML object."
        )

    print()
    print(f"Checking case: {case_id}")

    validate_case_paths(
        case_id=case_id,
        case_configuration=(
            case_configuration
        ),
    )

    ground_truth = load_case_ground_truth(
        case_configuration
    )

    if not isinstance(
        ground_truth,
        dict,
    ):
        raise ConfigurationValidationError(
            f"Ground truth for case '{case_id}' "
            "must contain a YAML object."
        )

    validate_case_id_match(
        configured_case_id=case_id,
        ground_truth=ground_truth,
    )

    validate_artifact_type(
        case_id=case_id,
        case_configuration=(
            case_configuration
        ),
        ground_truth=ground_truth,
    )

    ground_truth_items = (
        get_ground_truth_items(
            ground_truth
        )
    )

    if not ground_truth_items:
        raise ConfigurationValidationError(
            f"Case '{case_id}' has no "
            "ground-truth misconfigurations."
        )

    print(
        "  [OK] Ground-truth IDs: "
        + ", ".join(
            sorted(
                ground_truth_items.keys()
            )
        )
    )

    warning_count = validate_rule_mappings(
        case_id=case_id,
        case_configuration=(
            case_configuration
        ),
        ground_truth_items=(
            ground_truth_items
        ),
        configured_scanners=(
            configured_scanners
        ),
    )

    return warning_count


# This function validates the complete benchmark configuration.
def run_validation() -> int:
    """Validate the complete benchmark configuration."""

    print(
        "Validating benchmark configuration..."
    )

    print(f"Config: {CONFIG_PATH}")
    print()

    configuration = (
        load_benchmark_config()
    )

    if not isinstance(
        configuration,
        dict,
    ):
        raise ConfigurationValidationError(
            "The benchmark configuration root "
            "must be a YAML object."
        )

    validate_schema_version(
        configuration
    )

    (
        _matching_mode,
        configured_scanners,
    ) = validate_defaults(
        configuration
    )

    validate_optional_paths(
        configuration
    )

    cases = configuration.get(
        "cases"
    )

    if not isinstance(cases, dict):
        raise ConfigurationValidationError(
            "cases must be a YAML object."
        )

    if not cases:
        raise ConfigurationValidationError(
            "No benchmark cases are configured."
        )

    print(
        f"[OK] Benchmark cases found: "
        f"{len(cases)}"
    )

    total_warning_count = 0

    for case_id_value, case_configuration in (
        cases.items()
    ):
        case_id = clean_text(
            case_id_value
        )

        if case_id is None:
            raise ConfigurationValidationError(
                "A benchmark case has an invalid "
                "or empty case ID."
            )

        warning_count = validate_case(
            case_id=case_id,
            case_configuration=(
                case_configuration
            ),
            configured_scanners=(
                configured_scanners
            ),
        )

        total_warning_count += (
            warning_count
        )

    print()

    if total_warning_count:
        print(
            "Benchmark configuration validation "
            "passed with warnings."
        )

        print(
            "Warnings: "
            f"{total_warning_count}"
        )

        print(
            "Empty rule mappings are allowed during "
            "scanner-rule discovery. Populate them "
            "before running the final benchmark."
        )

    else:
        print(
            "Benchmark configuration "
            "validation passed."
        )

    return 0


# This function serves as the application entry point and handles any errors.
def main() -> int:
    """Application entry point."""

    try:
        return run_validation()

    except (
        ConfigurationError,
        ConfigurationValidationError,
    ) as error:
        print()
        print(
            "Benchmark configuration "
            "validation failed."
        )

        print(f"Reason: {error}")

        return 1

    except KeyboardInterrupt:
        print()
        print(
            "Configuration validation "
            "cancelled."
        )

        return 130

    except Exception as error:
        print()
        print(
            "Unexpected configuration "
            "validation error."
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())
