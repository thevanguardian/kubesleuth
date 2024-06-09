import argparse
from kubernetes import config
from outputs.json_output import results_to_json
from outputs.markdown_output import results_to_markdown
from tasks import *

# Load Kubernetes configuration
def load_kube_config(kubeconfig=None, context=None):
    if kubeconfig and context:
        config.load_kube_config(config_file=kubeconfig, context=context)
    elif kubeconfig:
        config.load_kube_config(config_file=kubeconfig)
    elif context:
        config.load_kube_config(context=context)
    else:
        config.load_kube_config()

# Filter issues by severity level
def filter_issues_by_level(issues, level):
    if level == 'all':
        return issues
    return [issue for issue in issues if issue['severity'].lower() == level]

# Main audit function
def audit_kubernetes(kubeconfig=None, context=None):
    load_kube_config(kubeconfig, context)
    audit_results = {"issues": []}

    checks = [
        check_rbac,
        check_password_auth,
        check_custom_roles,
        check_network_policies,
        check_namespace_isolation,
        check_privileged_containers,
        check_versions,
    ]

    for check in checks:
        result = check()
        if result:
            audit_results.update(result)
            audit_results["issues"].extend(result.get("issues", []))

    return audit_results

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Kubernetes Configuration Audit by KubeSleuth")
    parser.add_argument("--output", choices=["json", "markdown"], default="json", help="Output format (json or markdown)")
    parser.add_argument("--kubeconfig", help="Path to the kubeconfig file", default=None)
    parser.add_argument("--context", help="Kubernetes context to use", default=None)
    parser.add_argument("--level", choices=["high", "medium", "low", "all"], default="all", help="Assessment level to display")
    args = parser.parse_args()

    audit_results = audit_kubernetes(kubeconfig=args.kubeconfig, context=args.context)
    filtered_issues = filter_issues_by_level(audit_results["issues"], args.level)
    audit_results["issues"] = filtered_issues

    if args.output == "json":
        print(results_to_json(audit_results))
    else:
        print(results_to_markdown(audit_results))

if __name__ == "__main__":
    main()
