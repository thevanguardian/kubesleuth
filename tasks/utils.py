"""
Utility functions for working with Kubernetes.

The `append_issue` function adds a new issue to a list of issues, with optional namespace, name, and pod information.

The `load_kube_config` function loads the Kubernetes configuration from a specified kubeconfig file or context.
"""
from kubernetes import config
from typing import List, Dict, Optional

def append_issue(issues: List[Dict[str, Optional[str]]], issue: str, severity: str, namespace: Optional[str] = None, name: Optional[str] = None, pod: Optional[str] = None) -> None:
    issues.append({
        "issue": issue,
        "severity": severity,
        "namespace": namespace,
        "name": name,
        "pod": pod
    })

def load_kube_config(kubeconfig: Optional[str] = None, context: Optional[str] = None) -> None:
    if kubeconfig and context:
        config.load_kube_config(config_file=kubeconfig, context=context)
    elif kubeconfig:
        config.load_kube_config(config_file=kubeconfig)
    elif context:
        config.load_kube_config(context=context)
    else:
        config.load_kube_config()

# Example usage for debugging
if __name__ == "__main__":
    issues = []
    append_issue(issues, "Test issue", "High", namespace="default", name="test-name", pod="test-pod")
    print(issues)
    
    load_kube_config()
