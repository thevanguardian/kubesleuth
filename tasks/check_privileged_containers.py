"""
Checks for privileged containers in the Kubernetes cluster and returns a dictionary with the list of privileged containers and a list of issues found.

Returns:
    dict: A dictionary with the following keys:
        - "privileged_containers": A list of strings representing the namespaces and names of pods with privileged containers.
        - "issues": A list of dictionaries, where each dictionary represents an issue found and has the following keys:
            - "message": A string describing the issue.
            - "severity": A string representing the severity of the issue ("High", "Medium", or "Low").
            - "namespace": The namespace of the pod where the issue was found.
            - "name": The name of the pod where the issue was found.
"""
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue

def check_privileged_containers() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()

    v1 = client.CoreV1Api()
    try:
        privileged_containers = []
        pods = v1.list_pod_for_all_namespaces().items
        for pod in pods:
            for container in pod.spec.containers:
                if container.security_context and container.security_context.privileged:
                    privileged_containers.append(f"{pod.metadata.namespace}/{pod.metadata.name}")
                    append_issue(issues, "Container is running with privileged access.", "High", namespace=pod.metadata.namespace, name=pod.metadata.name)
                
                # Check for industry best practices for containers
                if not container.security_context:
                    append_issue(issues, "Container has no security context defined.", "Medium", namespace=pod.metadata.namespace, name=pod.metadata.name)
                else:
                    if container.security_context.run_as_user is None:
                        append_issue(issues, "Container is not running as a specific user.", "Medium", namespace=pod.metadata.namespace, name=pod.metadata.name)
                    if container.security_context.run_as_non_root is None or not container.security_context.run_as_non_root:
                        append_issue(issues, "Container is not configured to run as non-root.", "High", namespace=pod.metadata.namespace, name=pod.metadata.name)
                    if container.security_context.read_only_root_filesystem is None or not container.security_context.read_only_root_filesystem:
                        append_issue(issues, "Container root filesystem is not read-only.", "Medium", namespace=pod.metadata.namespace, name=pod.metadata.name)

        return {"privileged_containers": privileged_containers, "issues": issues}
    except ApiException as e:
        print(f"Exception when checking privileged containers: {e}")
        return {"privileged_containers": [], "issues": issues}
    finally:
        v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_privileged_containers()
    print(result)
