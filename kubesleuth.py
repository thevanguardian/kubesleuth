import argparse
from outputs import results_to_json, results_to_markdown, results_to_yaml
from tasks import *

# Define available checks
available_checks = {
    'rbac': check_rbac,
    'password_auth': check_password_auth,
    'custom_roles': check_custom_roles,
    'network_policies': check_network_policies,
    'namespace_isolation': check_namespace_isolation,
    'privileged_containers': check_privileged_containers,
    'versions': check_versions,
    'node_health': check_node_health
}

# Filter issues by severity level
def filter_issues_by_level(issues, level):
    if level == 'all':
        return issues
    elif level == 'debug':
        return issues  # In debug mode, include all issues and info
    return [issue for issue in issues if issue['severity'].lower() == level or (level == 'info' and issue['severity'].lower() == 'info')]

# Main audit function
def audit_kubernetes(kubeconfig=None, context=None, selected_checks=None):
    load_kube_config(kubeconfig, context)
    audit_results = {"issues": []}

    if not selected_checks:
        selected_checks = available_checks.keys()

    for check_name in selected_checks:
        check = available_checks.get(check_name)
        if check:
            result = check()
            if result:
                audit_results.update(result)
                audit_results["issues"].extend(result.get("issues", []))

    return audit_results

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Kubernetes Configuration Audit by KubeSleuth")
    parser.add_argument("--output", choices=["json", "markdown", "yaml"], default="json", help="Output format (json, markdown, or yaml)")
    parser.add_argument("--kubeconfig", help="Path to the kubeconfig file", default=None)
    parser.add_argument("--context", help="Kubernetes context to use", default=None)
    parser.add_argument("--level", choices=["high", "medium", "low", "all", "debug"], default="all", help="Assessment level to display")
    parser.add_argument(
        "--checks",
        nargs='+',
        choices=list(available_checks.keys()),
        metavar='CHECK',
        help="List of checks to run (choices: {})".format(", ".join(available_checks.keys()))
    )
    args = parser.parse_args()

    audit_results = audit_kubernetes(kubeconfig=args.kubeconfig, context=args.context, selected_checks=args.checks)
    filtered_issues = filter_issues_by_level(audit_results["issues"], args.level)
    audit_results["issues"] = filtered_issues

    if args.output == "json":
        print(results_to_json(audit_results))
    elif args.output == "markdown":
        print(results_to_markdown(audit_results))
    elif args.output == "yaml":
        print(results_to_yaml(audit_results))

if __name__ == "__main__":
    main()
