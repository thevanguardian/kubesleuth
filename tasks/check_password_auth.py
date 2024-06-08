"""
Checks if basic authentication is enabled for the Kubernetes API server.

Returns:
    dict: A dictionary with the following keys:
        - 'password_auth': 'enabled' if basic authentication is enabled, 'disabled' otherwise.
        - 'issues': A list of issues found, if any.
"""
from kubernetes import client
from kubernetes.client.rest import ApiException
from .utils import append_issue

def check_password_auth():
    v1 = client.CoreV1Api()
    issues = []
    try:
        config_maps = v1.list_namespaced_config_map("kube-system").items
        for cm in config_maps:
            if "kube-apiserver" in cm.metadata.name:
                if "data" in cm.data:
                    api_server_config = cm.data["data"]
                    if "--basic-auth-file" in api_server_config:
                        append_issue(issues, "Basic authentication is enabled.", "High")
                        return {"password_auth": "enabled", "issues": issues}
        return {"password_auth": "disabled", "issues": issues}
    except ApiException as e:
        print(f"Exception when checking password authentication: {e}")
        return None
