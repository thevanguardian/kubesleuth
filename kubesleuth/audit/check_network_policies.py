from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any, List
from .utils import append_issue

def check_network_policies() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    networking_v1 = client.NetworkingV1Api()
    core_v1 = client.CoreV1Api()

    try:
        namespaces = core_v1.list_namespace().items
        for namespace in namespaces:
            namespace_name = namespace.metadata.name
            netpols = networking_v1.list_namespaced_network_policy(namespace_name).items

            # Generate Info issues for all network policies
            for netpol in netpols:
                append_issue(issues, f"netpol/{netpol.metadata.name}", namespace_name, "Network policy found in namespace.", "Info")

            # Check if no network policies are in place
            if not netpols:
                append_issue(issues, f"netpol/none", namespace_name, "No network policies are in place.", "High")
            else:
                # Validate network policies for best practices
                for netpol in netpols:
                    if not netpol.spec.pod_selector.match_labels:
                        append_issue(issues, f"netpol/{netpol.metadata.name}", namespace_name, "Network policy does not specify pod selectors.", "Medium")

                    if not netpol.spec.policy_types or 'Ingress' not in netpol.spec.policy_types or 'Egress' not in netpol.spec.policy_types:
                        append_issue(issues, f"netpol/{netpol.metadata.name}", namespace_name, "Network policy should specify both Ingress and Egress policy types.", "Medium")

                    if not netpol.spec.ingress:
                        append_issue(issues, f"netpol/{netpol.metadata.name}", namespace_name, "Network policy does not define any ingress rules.", "Medium")

                    if not netpol.spec.egress:
                        append_issue(issues, f"netpol/{netpol.metadata.name}", namespace_name, "Network policy does not define any egress rules.", "Medium")

        return {"issues": issues}
    except ApiException as e:
        print(f"Exception when checking network policies: {e}")
        return {"issues": issues}
    finally:
        core_v1.api_client.close()
        networking_v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_network_policies()
    print(result)
