"""
Converts a dictionary of results to a YAML string.

Args:
    results (Dict[str, Any]): A dictionary of results to be converted to YAML.

Returns:
    str: The YAML string representation of the results dictionary.
"""
import yaml
from typing import Any, Dict

def results_to_yaml(results: Dict[str, Any]) -> str:
    return yaml.dump(results, default_flow_style=False, sort_keys=False)
