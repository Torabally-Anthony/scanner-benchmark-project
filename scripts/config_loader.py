from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = (
    PROJECT_ROOT
    / "config"
    / "benchmark_config.yaml"
)


class ConfigurationError(Exception):
    """Raised when the benchmark configuration is invalid."""


# This function loads a YAML file and confirms its root is an object.
def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file and confirm its root is an object."""

    if not path.exists():
        raise ConfigurationError(
            f"File does not exist: {path}"
        )

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            data = yaml.safe_load(file)

    except yaml.YAMLError as error:
        raise ConfigurationError(
            f"Invalid YAML in {path.name}: {error}"
        ) from error

    if not isinstance(data, dict):
        raise ConfigurationError(
            f"The root of {path.name} must be a YAML object."
        )

    return data


# This function loads the central benchmark configuration.
def load_benchmark_config() -> dict[str, Any]:
    """Load the central benchmark configuration."""

    configuration = load_yaml(CONFIG_PATH)

    if str(configuration.get("schema_version")) != "1.0":
        raise ConfigurationError(
            "Unsupported benchmark configuration schema."
        )

    return configuration


# This function returns the configuration for one benchmark case.
def get_case_configuration(
    configuration: dict[str, Any],
    case_id: str,
) -> dict[str, Any]:
    """Return the configuration for one benchmark case."""

    cases = configuration.get("cases")

    if not isinstance(cases, dict):
        raise ConfigurationError(
            "The benchmark configuration has no valid cases."
        )

    case_configuration = cases.get(case_id)

    if not isinstance(case_configuration, dict):
        raise ConfigurationError(
            f"Unknown benchmark case: {case_id}"
        )

    return case_configuration


# This function resolves a configuration path against the project root.
def resolve_project_path(path_value: str) -> Path:
    """Resolve a configuration path against the project root."""

    if not isinstance(path_value, str) or not path_value.strip():
        raise ConfigurationError(
            "A required project path is missing."
        )

    path = (PROJECT_ROOT / path_value).resolve()

    # Reject path traversal so configuration cannot reference files outside the project.
    try:
        path.relative_to(PROJECT_ROOT)
    except ValueError as error:
        raise ConfigurationError(
            f"Path is outside the project directory: {path}"
        ) from error

    return path


# This function loads the ground-truth file configured for a case.
def load_case_ground_truth(
    case_configuration: dict[str, Any],
) -> dict[str, Any]:
    """Load the ground-truth file configured for a case."""

    ground_truth_value = case_configuration.get(
        "ground_truth_path"
    )

    if not isinstance(ground_truth_value, str):
        raise ConfigurationError(
            "The case has no ground_truth_path."
        )

    ground_truth_path = resolve_project_path(
        ground_truth_value
    )

    return load_yaml(ground_truth_path)


# This function indexes ground-truth items by their IDs.
def get_ground_truth_items(
    ground_truth: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Index ground-truth items by their IDs."""

    misconfigurations = ground_truth.get(
        "misconfigurations"
    )

    if not isinstance(misconfigurations, list):
        raise ConfigurationError(
            "Ground truth must contain a "
            "'misconfigurations' list."
        )

    indexed_items: dict[str, dict[str, Any]] = {}

    for item in misconfigurations:
        if not isinstance(item, dict):
            continue

        ground_truth_id = item.get("id")

        if (
            isinstance(ground_truth_id, str)
            and ground_truth_id.strip()
        ):
            indexed_items[ground_truth_id.strip()] = item

    if not indexed_items:
        raise ConfigurationError(
            "No valid ground-truth items were found."
        )

    return indexed_items


# This function converts scanner rule mappings into a lookup from rule IDs to ground-truth IDs.
def build_rule_to_ground_truth_map(
    case_configuration: dict[str, Any],
    scanner: str,
) -> dict[str, str]:
    """
    Convert the configuration into:

    scanner rule ID -> ground-truth ID
    """

    mappings = case_configuration.get("rule_mappings")

    if not isinstance(mappings, dict):
        raise ConfigurationError(
            "The case has no valid rule_mappings."
        )

    reverse_mapping: dict[str, str] = {}

    for ground_truth_id, scanner_mappings in mappings.items():
        if not isinstance(scanner_mappings, dict):
            continue

        rule_ids = scanner_mappings.get(scanner, [])

        if not isinstance(rule_ids, list):
            raise ConfigurationError(
                f"Rules for scanner '{scanner}' must be a list."
            )

        for rule_id in rule_ids:
            if not isinstance(rule_id, str):
                continue

            clean_rule_id = rule_id.strip()

            if not clean_rule_id:
                continue

            previous_mapping = reverse_mapping.get(
                clean_rule_id
            )

            # One rule cannot identify two expected issues because the match would be ambiguous.
            if (
                previous_mapping is not None
                and previous_mapping != ground_truth_id
            ):
                raise ConfigurationError(
                    f"Scanner rule '{clean_rule_id}' maps to "
                    "more than one ground-truth ID."
                )

            reverse_mapping[clean_rule_id] = str(
                ground_truth_id
            )

    return reverse_mapping
