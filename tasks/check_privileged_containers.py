"""
Checks for privileged containers in the Kubernetes cluster and returns a dictionary with the list of privileged containers and any issues found.

Returns:
    dict: A dictionary with the following keys:
        - "privileged_containers": A list of strings representing the namespaces and names of pods with privileged containers.
        - "issues": A list of dictionaries, where each dictionary represents an issue found, with the following keys:
            - "message": A string describing the issue.
            - "severity": A string representing the severity of the issue ("High", "Medium", or "Low").
            - "namespace": The namespace of the pod with the issue.
            - "pod": The name of the pod with the issue.
    None: If an exception occurs while checking for privileged containers.
"""
from kubernetes import client
from kubernetes.client.rest import ApiException
from .utils import append_issue

def check_privileged_containers():
    v1 = client.CoreV1Api()
    privileged_containers = []
    issues = []
    try:
        pods = v1.list_pod_for_all_namespaces().items
        for pod in pods:
            for container in pod.spec.containers:
                if container.security_context and container.security_context.privileged:
                    privileged_containers.append(f"{pod.metadata.namespace}/{pod.metadata.name}")
                    append_issue(issues, "Container is running with privileged access.", "High", namespace=pod.metadata.namespace, pod=pod.metadata.name)
        return {"privileged_containers": privileged_containers, "issues": issues}
    except ApiException as e:
        print(f"Exception when checking privileged containers: {e}")
        return None
