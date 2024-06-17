from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
import os

def results_to_markdown(results: Dict[str, Any]) -> str:
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

    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__) + '/../templates'))
    template = env.get_template('audit_template.md.j2')
    markdown_output = template.render(results=filtered_results)
    return markdown_output
