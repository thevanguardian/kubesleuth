"""
Loads the Kubernetes configuration based on the provided kubeconfig file and context.

Args:
    kubeconfig (str, optional): Path to the kubeconfig file. If not provided, the default kubeconfig file will be used.
    context (str, optional): Kubernetes context to use. If not provided, the default context will be used.

Raises:
    Exception: If there is an error loading the Kubernetes configuration.
"""

"""
Performs a comprehensive audit of the Kubernetes cluster configuration.

Args:
    kubeconfig (str, optional): Path to the kubeconfig file. If not provided, the default kubeconfig file will be used.
    context (str, optional): Kubernetes context to use. If not provided, the default context will be used.

Returns:
    dict: A dictionary containing the audit results, including any issues found.
"""
import argparse
from outputs.json_output import results_to_json
from outputs.markdown_output import results_to_markdown
from tasks import *
from kubernetes import config

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
        # Add other checks here
    ]

    for check in checks:
        result = check()
        if result:
            audit_results.update(result)
            audit_results["issues"].extend(result.get("issues", []))

    return audit_results

# Command-line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kubernetes Configuration Audit")
    parser.add_argument("--output", choices=["json", "markdown"], default="json", help="Output format (json or markdown)")
    parser.add_argument("--kubeconfig", help="Path to the kubeconfig file", default=None)
    parser.add_argument("--context", help="Kubernetes context to use", default=None)
    args = parser.parse_args()

    audit_results = audit_kubernetes(kubeconfig=args.kubeconfig, context=args.context)

    if args.output == "json":
        print(results_to_json(audit_results))
    else:
        print(results_to_markdown(audit_results))
