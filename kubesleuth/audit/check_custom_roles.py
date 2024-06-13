from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any, List
from .utils import append_issue

# Check if the role is a default Kubernetes role
def is_default_role(role_name: str) -> bool:
    default_roles = [
        "cluster-admin", "admin", "edit", "view", "system:node", 
        "system:node-proxier", "system:node-bootstrapper", 
        "system:certificates.k8s.io:certificatesigningrequests:nodeclient",
        "system:certificates.k8s.io:certificatesigningrequests:selfnodeclient"
    ]
    return role_name in default_roles

# Check if the role has overly broad permissions
def has_overly_broad_permissions(role) -> bool:
    for rule in role.rules:
        if ('*' in (rule.verbs or []) or 
            '*' in (rule.api_groups or []) or 
            '*' in (rule.resources or [])):
            return True
    return False

# Main function to check custom roles
def check_custom_roles() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()

    rbac_v1 = client.RbacAuthorizationV1Api()
    try:
        roles = rbac_v1.list_role_for_all_namespaces().items
        cluster_roles = rbac_v1.list_cluster_role().items
        role_bindings = rbac_v1.list_role_binding_for_all_namespaces().items
        cluster_role_bindings = rbac_v1.list_cluster_role_binding().items

        custom_roles = [role for role in roles if not is_default_role(role.metadata.name)]
        custom_cluster_roles = [cr for cr in cluster_roles if not is_default_role(cr.metadata.name)]

        custom_role_count = len(custom_roles) + len(custom_cluster_roles)

        # Check for default roles in role bindings
        default_role_bindings = [
            rb for rb in role_bindings 
            if is_default_role(rb.role_ref.name)
        ] + [
            crb for crb in cluster_role_bindings 
            if is_default_role(crb.role_ref.name)
        ]

        # Check for overly broad permissions in custom roles
        overly_broad_custom_roles = [
            role for role in custom_roles + custom_cluster_roles 
            if has_overly_broad_permissions(role)
        ]

        if custom_role_count == 0:
            if default_role_bindings:
                append_issue(issues, "role/unknown", "default", "No custom roles exist and default roles are in use.", "High")
            else:
                append_issue(issues, "role/unknown", "default", "No custom roles exist and no default roles are in use.", "Medium")
        elif custom_role_count <= 2:
            append_issue(issues, "role/unknown", "default", "Only one or two custom roles exist.", "Low")
        else:
            append_issue(issues, "role/unknown", "default", f"{custom_role_count} custom roles found.", "Info")

        if overly_broad_custom_roles:
            for role in overly_broad_custom_roles:
                append_issue(issues, f"role/{role.metadata.name}", role.metadata.namespace, "Role has overly broad permissions.", "High")

        # Adding details of all custom roles and role bindings for debugging
        append_issue(issues, "role/unknown", "default", f"Custom roles: {[role.metadata.name for role in custom_roles]}", "Info")
        append_issue(issues, "role/unknown", "default", f"Custom cluster roles: {[cr.metadata.name for cr in custom_cluster_roles]}", "Info")
        append_issue(issues, "role/unknown", "default", f"Default role bindings: {[rb.metadata.name for rb in default_role_bindings]}", "Info")

        return {"issues": issues}
    except ApiException as e:
        print(f"Exception when checking custom roles: {e}")
        return {"issues": issues}
    finally:
        rbac_v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_custom_roles()
    print(result)
