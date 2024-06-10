from kubernetes import client, config
from typing import Dict, Any
from .utils import append_issue

def check_password_auth() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    try:
        # Assuming password authentication configurations are stored in a ConfigMap named "auth-config" in the "kube-system" namespace
        auth_config = core_v1.read_namespaced_config_map("auth-config", "kube-system")

        # Generate Info issues for all password configurations
        for key, value in auth_config.data.items():
            append_issue(issues, f"auth-config/{key}", "kube-system", f"Password configuration: {key} = {value}", "Info")

        # Best practices checks
        if auth_config.data.get("password_auth") == "enabled":
            append_issue(issues, "auth/password", "kube-system", "Password authentication is enabled.", "High")

        if "min_password_length" in auth_config.data:
            if int(auth_config.data["min_password_length"]) < 12:
                append_issue(issues, "auth/min_password_length", "kube-system", "Minimum password length is less than 12 characters.", "Medium")

        if "password_complexity" in auth_config.data:
            complexity = auth_config.data["password_complexity"]
            if not all(char in complexity for char in ["upper", "lower", "digit", "special"]):
                append_issue(issues, "auth/password_complexity", "kube-system", "Password complexity requirements are not comprehensive (should include upper, lower, digit, and special characters).", "Medium")

        if "password_rotation_days" in auth_config.data:
            if int(auth_config.data["password_rotation_days"]) > 90:
                append_issue(issues, "auth/password_rotation_days", "kube-system", "Password rotation period is more than 90 days.", "Medium")

        if "mfa_enabled" in auth_config.data and auth_config.data["mfa_enabled"] == "false":
            append_issue(issues, "auth/mfa", "kube-system", "Multi-factor authentication (MFA) is not enabled.", "Medium")

    except client.exceptions.ApiException as e:
        if e.status == 404:
            append_issue(issues, "auth-config/missing", "kube-system", "ConfigMap 'auth-config' not found in 'kube-system' namespace.", "High")
        else:
            print(f"Exception when checking password authentication: {e}")

    finally:
        core_v1.api_client.close()

    return {"issues": issues}

# Example usage for debugging
if __name__ == "__main__":
    result = check_password_auth()
    print(result)
