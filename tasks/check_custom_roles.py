"""
Checks for the usage of default Kubernetes roles and cluster roles, and reports any issues found.

Returns:
    dict: A dictionary containing the following keys:
        - "roles": A list of dictionaries representing the Kubernetes roles found.
        - "cluster_roles": A list of dictionaries representing the Kubernetes cluster roles found.
        - "issues": A list of dictionaries representing any issues found, with the following keys:
            - "message": A description of the issue.
            - "severity": The severity of the issue ("High" or "Low").
            - "namespace": The namespace of the role (if applicable).
            - "name": The name of the role or cluster role.
"""
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue

def check_custom_roles() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    
    v1 = client.RbacAuthorizationV1Api()
    try:
        roles = v1.list_role_for_all_namespaces().items
        cluster_roles = v1.list_cluster_role().items

        for role in roles:
            if "system:" in role.metadata.name:
                append_issue(issues, "Default role is being used instead of a custom role.", "High", namespace=role.metadata.namespace, name=role.metadata.name)
            else:
                append_issue(issues, "Custom role is being used.", "Low", namespace=role.metadata.namespace, name=role.metadata.name)

        for cluster_role in cluster_roles:
            if "system:" in cluster_role.metadata.name:
                append_issue(issues, "Default cluster role is being used instead of a custom role.", "High", name=cluster_role.metadata.name)
            else:
                append_issue(issues, "Custom cluster role is being used.", "Low", name=cluster_role.metadata.name)

        return {
            "roles": [role.to_dict() for role in roles],
            "cluster_roles": [cr.to_dict() for cr in cluster_roles],
            "issues": issues
        }
    except ApiException as e:
        print(f"Exception when checking custom roles: {e}")
        return {
            "roles": [],
            "cluster_roles": [],
            "issues": issues
        }
    finally:
        v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_custom_roles()
    print(result)
