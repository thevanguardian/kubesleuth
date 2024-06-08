"""
Checks the RBAC (Role-Based Access Control) configuration in the Kubernetes cluster.

This function retrieves all RoleBindings and ClusterRoleBindings in the cluster, and checks if they have any subjects defined. If a RoleBinding or ClusterRoleBinding is found without any subjects, an issue is appended to the `issues` list.

The function returns a dictionary containing the following keys:
- `role_bindings`: a list of dictionaries representing all RoleBindings in the cluster
- `cluster_role_bindings`: a list of dictionaries representing all ClusterRoleBindings in the cluster
- `issues`: a list of dictionaries representing any issues found in the RBAC configuration

If an exception occurs while checking the RBAC configuration, the function will return `None`.
"""
from kubernetes import client
from kubernetes.client.rest import ApiException
from .utils import append_issue

def check_rbac():
    v1 = client.RbacAuthorizationV1Api()
    issues = []
    try:
        role_bindings = v1.list_role_binding_for_all_namespaces().items
        cluster_role_bindings = v1.list_cluster_role_binding().items
        for rb in role_bindings:
            if rb.subjects is None:
                append_issue(issues, "RoleBinding has no subjects.", "High", namespace=rb.metadata.namespace, name=rb.metadata.name)
        for crb in cluster_role_bindings:
            if crb.subjects is None:
                append_issue(issues, "ClusterRoleBinding has no subjects.", "High", name=crb.metadata.name)
        return {
            "role_bindings": [rb.to_dict() for rb in role_bindings],
            "cluster_role_bindings": [crb.to_dict() for crb in cluster_role_bindings],
            "issues": issues
        }
    except ApiException as e:
        print(f"Exception when checking RBAC: {e}")
        return None
