import yaml
from typing import Dict, Any

def results_to_yaml(results: Dict[str, Any]) -> str:
    filtered_issues = []
    for issue in results.get("issues", []):
        filtered_issue = {
            "name": issue.get("name"),
            "namespace": issue.get("namespace"),
            "fault": issue.get("fault"),
            "threat": issue.get("threat")
        }
        filtered_issues.append(filtered_issue)

    filtered_results = {"issues": filtered_issues}
    return yaml.dump(filtered_results, default_flow_style=False, sort_keys=False)
