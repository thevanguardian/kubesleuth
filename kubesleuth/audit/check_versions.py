from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
import requests
from .utils import append_issue

def get_latest_version(component: str) -> str:
    # Function to get the latest stable version of the component from an official source
    try:
        response = requests.get(f"https://storage.googleapis.com/kubernetes-release/release/stable.txt")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "unknown"
    except Exception as e:
        print(f"Error fetching latest version for {component}: {e}")
        return "unknown"

def check_versions() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    core_v1 = client.CoreV1Api()
    version_api = client.VersionApi()

    try:
        # Get current versions
        current_version = version_api.get_code()
        latest_version = get_latest_version("kubernetes")

        # Generate Info issue for the current version
        append_issue(issues, "version/kubernetes", "default", f"Current Kubernetes version: {current_version.git_version}", "Info")

        # Check if the current version is up-to-date
        if current_version.git_version != latest_version:
            append_issue(issues, "version/kubernetes", "default", f"Kubernetes version {current_version.git_version} is not up-to-date. Latest version is {latest_version}.", "Medium")

        # Example of checking other components, e.g., kubelet, etcd
        nodes = core_v1.list_node().items
        for node in nodes:
            kubelet_version = node.status.node_info.kubelet_version
            latest_kubelet_version = get_latest_version("kubelet")
            append_issue(issues, f"version/kubelet/{node.metadata.name}", "default", f"Kubelet version: {kubelet_version}", "Info")
            if kubelet_version != latest_kubelet_version:
                append_issue(issues, f"version/kubelet/{node.metadata.name}", "default", f"Kubelet version {kubelet_version} on node {node.metadata.name} is not up-to-date. Latest version is {latest_kubelet_version}.", "Medium")

        return {"issues": issues}
    except ApiException as e:
        print(f"Exception when checking versions: {e}")
        return {"issues": issues}
    finally:
        core_v1.api_client.close()
        version_api.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_versions()
    print(result)
