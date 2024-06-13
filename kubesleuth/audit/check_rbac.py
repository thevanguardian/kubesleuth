from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue

def check_rbac() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    rbac_v1 = client.RbacAuthorizationV1Api()

    try:
        # List all RoleBindings and ClusterRoleBindings
        role_bindings = rbac_v1.list_role_binding_for_all_namespaces().items
        cluster_role_bindings = rbac_v1.list_cluster_role_binding().items

        # Generate Info issues for all RBAC configurations
        for rb in role_bindings:
            append_issue(issues, f"rolebinding/{rb.metadata.name}", rb.metadata.namespace, "RoleBinding configuration found.", "Info")
        for crb in cluster_role_bindings:
            append_issue(issues, f"clusterrolebinding/{crb.metadata.name}", crb.metadata.namespace, "ClusterRoleBinding configuration found.", "Info")

        # Check for best practices in RoleBindings
        for rb in role_bindings:
            if rb.role_ref.kind == "ClusterRole":
                append_issue(issues, f"rolebinding/{rb.metadata.name}", rb.metadata.namespace, "RoleBinding binds to a ClusterRole.", "Medium")

            if rb.subjects:
                for subject in rb.subjects:
                    if subject.kind == "ServiceAccount" and subject.name == "default":
                        append_issue(issues, f"rolebinding/{rb.metadata.name}", rb.metadata.namespace, "RoleBinding binds to the default service account.", "High")

            # Check for wildcard permissions
            try:
                role = rbac_v1.read_namespaced_role(rb.role_ref.name, rb.metadata.namespace)
                for rule in role.rules:
                    if rule.verbs and '*' in rule.verbs:
                        append_issue(issues, f"rolebinding/{rb.metadata.name}", rb.metadata.namespace, "RoleBinding grants wildcard permissions for verbs.", "High")
                    if rule.resources and '*' in rule.resources:
                        append_issue(issues, f"rolebinding/{rb.metadata.name}", rb.metadata.namespace, "RoleBinding grants wildcard permissions for resources.", "High")
            except ApiException:
                append_issue(issues, f"rolebinding/{rb.metadata.name}", rb.metadata.namespace, "RoleBinding references a non-existent role.", "High")

        # Check for best practices in ClusterRoleBindings
        for crb in cluster_role_bindings:
            if crb.subjects:
                for subject in crb.subjects:
                    if subject.kind == "ServiceAccount" and subject.name == "default":
                        append_issue(issues, f"clusterrolebinding/{crb.metadata.name}", crb.metadata.namespace, "ClusterRoleBinding binds to the default service account.", "High")

            # Check for wildcard permissions
            try:
                cluster_role = rbac_v1.read_cluster_role(crb.role_ref.name)
                for rule in cluster_role.rules:
                    if rule.verbs and '*' in rule.verbs:
                        append_issue(issues, f"clusterrolebinding/{crb.metadata.name}", crb.metadata.namespace, "ClusterRoleBinding grants wildcard permissions for verbs.", "High")
                    if rule.resources and '*' in rule.resources:
                        append_issue(issues, f"clusterrolebinding/{crb.metadata.name}", crb.metadata.namespace, "ClusterRoleBinding grants wildcard permissions for resources.", "High")
            except ApiException:
                append_issue(issues, f"clusterrolebinding/{crb.metadata.name}", crb.metadata.namespace, "ClusterRoleBinding references a non-existent cluster role.", "High")

        return {"issues": issues}
    except ApiException as e:
        print(f"Exception when checking RBAC: {e}")
        return {"issues": issues}
    finally:
        rbac_v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_rbac()
    print(result)
