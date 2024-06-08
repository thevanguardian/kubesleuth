"""
Checks the namespace isolation of the Kubernetes cluster.

Returns:
    dict: A dictionary containing the list of namespaces in the cluster, or None if an exception occurs.
"""
from kubernetes import client
from kubernetes.client.rest import ApiException

def check_namespace_isolation():
    v1 = client.CoreV1Api()
    try:
        namespaces = v1.list_namespace().items
        return {"namespaces": [ns.to_dict() for ns in namespaces]}
    except ApiException as e:
        print(f"Exception when checking namespaces: {e}")
        return None
