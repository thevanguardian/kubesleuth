"""
Checks the network policies defined in the Kubernetes cluster.

Returns:
    dict: A dictionary containing the following keys:
        - "network_policies": A list of dictionaries representing the network policies.
        - "issues": A list of issues found with the network policies.
"""
from kubernetes import client
from kubernetes.client.rest import ApiException
from .utils import append_issue

def check_network_policies():
    v1 = client.NetworkingV1Api()
    issues = []
    try:
        netpols = v1.list_network_policy_for_all_namespaces().items
        if not netpols:
            append_issue(issues, "No network policies are defined.", "Medium")
        return {"network_policies": [np.to_dict() for np in netpols], "issues": issues}
    except ApiException as e:
        print(f"Exception when checking network policies: {e}")
        return None
