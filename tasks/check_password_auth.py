"""
Checks the password authentication configuration in the Kubernetes cluster.

Returns:
    dict: A dictionary containing the following keys:
        - 'password_auth': A boolean indicating whether password authentication is enabled.
        - 'issues': A list of issues found in the password authentication configuration.
"""
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue

def check_password_auth() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    
    v1 = client.CoreV1Api()
    try:
        config_maps = v1.list_namespaced_config_map("kube-system").items
        basic_auth_enabled = False
        for cm in config_maps:
            if "kube-apiserver" in cm.metadata.name:
                if "data" in cm.data:
                    api_server_config = cm.data["data"]
                    if "--basic-auth-file" in api_server_config:
                        append_issue(issues, "Basic authentication is enabled, which is insecure.", "High")
                        basic_auth_enabled = True
        
        if not basic_auth_enabled:
            append_issue(issues, "Basic authentication is not enabled.", "Low")
        
        # Best practices for password policies (Example)
        password_policies = {
            "min_length": 12,
            "complexity": True,  # Should include upper, lower, digits, special characters
            "rotation": 90,  # Password rotation policy in days
            "mfa": True  # Multi-factor authentication enabled
        }

        # Check if password policies are defined in ConfigMaps or Secrets
        for cm in config_maps:
            if "password-policy" in cm.metadata.name:
                # Example of checking password policies
                if "min_length" in cm.data and int(cm.data["min_length"]) < password_policies["min_length"]:
                    append_issue(issues, f"Password minimum length is less than {password_policies['min_length']}.", "High")
                if "complexity" in cm.data and cm.data["complexity"].lower() != str(password_policies["complexity"]).lower():
                    append_issue(issues, "Password complexity requirements are not enforced.", "High")
                if "rotation" in cm.data and int(cm.data["rotation"]) > password_policies["rotation"]:
                    append_issue(issues, f"Password rotation period is more than {password_policies['rotation']} days.", "Medium")
                if "mfa" in cm.data and cm.data["mfa"].lower() != str(password_policies["mfa"]).lower():
                    append_issue(issues, "Multi-factor authentication is not enabled.", "High")

        return {"password_auth": not basic_auth_enabled, "issues": issues}
    except ApiException as e:
        print(f"Exception when checking password authentication: {e}")
        return {"password_auth": False, "issues": issues}
    finally:
        v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_password_auth()
    print(result)
