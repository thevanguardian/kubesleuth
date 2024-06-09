"""
Checks the RBAC (Role-Based Access Control) configuration of a Kubernetes cluster.

This function retrieves all RoleBindings and ClusterRoleBindings in the cluster, and checks for potential issues, such as:
- RoleBindings or ClusterRoleBindings that have no subjects
- RoleBindings or ClusterRoleBindings that bind to the default service account
- RoleBindings that refer to a ClusterRole instead of a Role
- ClusterRoleBindings that refer to a Role instead of a ClusterRole

The function returns a dictionary containing the list of RoleBindings, ClusterRoleBindings, and any issues found.

Returns:
    dict: A dictionary containing the following keys:
        - "role_bindings": A list of RoleBinding objects (as dictionaries)
        - "cluster_role_bindings": A list of ClusterRoleBinding objects (as dictionaries)
        - "issues": A list of dictionaries, each containing information about an issue found
"""
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue

def check_rbac() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()

    v1 = client.RbacAuthorizationV1Api()
    try:
        role_bindings = v1.list_role_binding_for_all_namespaces().items
        cluster_role_bindings = v1.list_cluster_role_binding().items

        # Check RoleBindings
        for rb in role_bindings:
            if rb.subjects is None:
                append_issue(issues, "RoleBinding has no subjects.", "High", namespace=rb.metadata.namespace, name=rb.metadata.name)
            else:
                for subject in rb.subjects:
                    if subject.kind == "ServiceAccount" and subject.name == "default":
                        append_issue(issues, "RoleBinding binds to the default service account.", "High", namespace=rb.metadata.namespace, name=rb.metadata.name)
            # Example best practice: Ensure RoleBindings are namespace-specific
            if rb.role_ref.kind == "ClusterRole":
                append_issue(issues, "RoleBinding refers to a ClusterRole instead of a Role.", "Medium", namespace=rb.metadata.namespace, name=rb.metadata.name)

        # Check ClusterRoleBindings
        for crb in cluster_role_bindings:
            if crb.subjects is None:
                append_issue(issues, "ClusterRoleBinding has no subjects.", "High", name=crb.metadata.name)
            else:
                for subject in crb.subjects:
                    if subject.kind == "ServiceAccount" and subject.name == "default":
                        append_issue(issues, "ClusterRoleBinding binds to the default service account.", "High", name=crb.metadata.name)
            # Example best practice: Ensure ClusterRoleBindings are used only when necessary
            if crb.role_ref.kind != "ClusterRole":
                append_issue(issues, "ClusterRoleBinding refers to a Role instead of a ClusterRole.", "Medium", name=crb.metadata.name)

        return {
            "role_bindings": [rb.to_dict() for rb in role_bindings],
            "cluster_role_bindings": [crb.to_dict() for crb in cluster_role_bindings],
            "issues": issues
        }
    except ApiException as e:
        print(f"Exception when checking RBAC: {e}")
        return {
            "role_bindings": [],
            "cluster_role_bindings": [],
            "issues": issues
        }
    finally:
        v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_rbac()
    print(result)
