"""
Checks for namespace isolation issues in a Kubernetes cluster.

This function retrieves all namespaces, pods, and services in the cluster, and checks for any resources running in the default namespace. It appends any issues found to a list and returns the list of issues along with a list of all namespaces.

Returns:
    dict: A dictionary containing the following keys:
        - "namespaces": A list of dictionaries representing the namespaces in the cluster.
        - "issues": A list of dictionaries representing any issues found, with the following keys:
            - "message": A description of the issue.
            - "severity": The severity of the issue ("High" or "Low").
            - "namespace": The namespace where the issue was found.
            - "name": The name of the resource where the issue was found (for pods and services).
"""
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue

def check_namespace_isolation() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()

    v1 = client.CoreV1Api()
    try:
        namespaces = v1.list_namespace().items
        for ns in namespaces:
            if ns.metadata.name == "default":
                append_issue(issues, "Resources should not be placed in the default namespace.", "High", namespace=ns.metadata.name)
            else:
                append_issue(issues, "Namespace is isolated.", "Low", namespace=ns.metadata.name)

        pods = v1.list_pod_for_all_namespaces().items
        for pod in pods:
            if pod.metadata.namespace == "default":
                append_issue(issues, "Pod is running in the default namespace.", "High", namespace=pod.metadata.namespace, name=pod.metadata.name)

        services = v1.list_service_for_all_namespaces().items
        for svc in services:
            if svc.metadata.namespace == "default":
                append_issue(issues, "Service is running in the default namespace.", "High", namespace=svc.metadata.namespace, name=svc.metadata.name)

        return {
            "namespaces": [ns.to_dict() for ns in namespaces],
            "issues": issues
        }
    except ApiException as e:
        print(f"Exception when checking namespace isolation: {e}")
        return {
            "namespaces": [],
            "issues": issues
        }
    finally:
        v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_namespace_isolation()
    print(result)
