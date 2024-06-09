"""
Checks the network policies in the Kubernetes cluster and returns a dictionary with the network policies and any issues found.

Returns:
    dict: A dictionary with the following keys:
        "network_policies": A list of dictionaries representing the network policies in the cluster.
        "issues": A list of dictionaries representing any issues found with the network policies.
            Each issue dictionary has the following keys:
                "message": A string describing the issue.
                "severity": A string indicating the severity of the issue ("High", "Medium", or "Low").
                "namespace": The namespace of the network policy (if applicable).
                "name": The name of the network policy (if applicable).
"""
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue

def check_network_policies() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    
    v1 = client.NetworkingV1Api()
    try:
        netpols = v1.list_network_policy_for_all_namespaces().items
        if not netpols:
            append_issue(issues, "No network policies are defined.", "High")
        else:
            for np in netpols:
                if not np.spec:
                    append_issue(issues, "Network policy has no spec defined.", "Medium", namespace=np.metadata.namespace, name=np.metadata.name)
                elif not np.spec.pod_selector:
                    append_issue(issues, "Network policy has no pod selector defined.", "Medium", namespace=np.metadata.namespace, name=np.metadata.name)
                elif not np.spec.policy_types:
                    append_issue(issues, "Network policy has no policy types defined.", "Medium", namespace=np.metadata.namespace, name=np.metadata.name)
                elif not np.spec.ingress and not np.spec.egress:
                    append_issue(issues, "Network policy has neither ingress nor egress rules defined.", "Medium", namespace=np.metadata.namespace, name=np.metadata.name)
                else:
                    append_issue(issues, "Network policy is appropriately configured.", "Low", namespace=np.metadata.namespace, name=np.metadata.name)

        return {
            "network_policies": [np.to_dict() for np in netpols],
            "issues": issues
        }
    except ApiException as e:
        print(f"Exception when checking network policies: {e}")
        return {
            "network_policies": [],
            "issues": issues
        }
    finally:
        v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_network_policies()
    print(result)
