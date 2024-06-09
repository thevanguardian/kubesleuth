"""
Checks the Kubernetes server version and compares it to the latest stable version.

Returns:
    dict: A dictionary containing the following keys:
        - 'server_version': The version of the Kubernetes server.
        - 'latest_version': The latest stable version of Kubernetes.
        - 'issues': A list of issues found, such as the server being out of date.
"""
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue
import requests

def check_versions() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()

    try:
        version_info = client.VersionApi().get_code()
        server_version = version_info.git_version

        # Check the compatibility and latest version dynamically
        latest_version_url = "https://storage.googleapis.com/kubernetes-release/release/stable.txt"
        response = requests.get(latest_version_url)
        response.raise_for_status()
        latest_version = response.text.strip()

        if server_version != latest_version:
            append_issue(issues, f"Kubernetes server is out of date. Current version: {server_version}, Latest version: {latest_version}.", "High")

        # Optionally, you can check the version compatibility matrix
        compatibility_url = "https://kubernetes.io/docs/setup/release/version-skew-policy/"
        append_issue(issues, f"Check Kubernetes version compatibility at: {compatibility_url}.", "Info")

        return {"server_version": server_version, "latest_version": latest_version, "issues": issues}
    except ApiException as e:
        print(f"Exception when checking versions: {e}")
        return {"server_version": None, "latest_version": None, "issues": issues}
    except requests.RequestException as e:
        print(f"Exception when fetching latest Kubernetes version: {e}")
        append_issue(issues, "Could not fetch the latest Kubernetes version information.", "High")
        return {"server_version": None, "latest_version": None, "issues": issues}

# Example usage for debugging
if __name__ == "__main__":
    result = check_versions()
    print(result)
