import json
from typing import Dict, Any

def results_to_json(results: Dict[str, Any]) -> str:
    # Extract only necessary information for each issue
    filtered_issues = []
    for issue in results.get("issues", []):
        filtered_issue = {
            "name": issue.get("name"),
            "namespace": issue.get("namespace"),
            "fault": issue.get("fault"),
            "severity": issue.get("severity")
        }
        filtered_issues.append(filtered_issue)

    filtered_results = {"issues": filtered_issues}
    return json.dumps(filtered_results, indent=4)
