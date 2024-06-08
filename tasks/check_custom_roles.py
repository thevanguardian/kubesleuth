"""
Checks for the existence of custom Kubernetes roles and cluster roles.

Returns:
    dict: A dictionary containing the following keys:
        - "roles": A list of dictionaries representing the custom roles in the cluster.
        - "cluster_roles": A list of dictionaries representing the custom cluster roles in the cluster.
        - "issues": A list of any issues encountered while checking the custom roles (currently empty).
    None: If an exception occurs while checking the custom roles.
"""
from kubernetes import client
from kubernetes.client.rest import ApiException

def check_custom_roles():
    v1 = client.RbacAuthorizationV1Api()
    try:
        roles = v1.list_role_for_all_namespaces().items
        cluster_roles = v1.list_cluster_role().items
        return {
            "roles": [role.to_dict() for role in roles],
            "cluster_roles": [cr.to_dict() for cr in cluster_roles],
            "issues": []  # Add logic for issues if needed
        }
    except ApiException as e:
        print(f"Exception when checking custom roles: {e}")
        return None
