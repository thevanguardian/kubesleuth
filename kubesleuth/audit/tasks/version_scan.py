"""
Implementation Plan for Version Scan Task
- Load Kubernetes Configuration: Load the Kubernetes configuration to access the cluster.
- Retrieve Component Versions: Fetch current versions of Kubernetes components.
- Fetch Latest Stable Version: Retrieve the latest stable version of Kubernetes from the official source.
- Compare Versions: Compare current versions against the latest stable version.
- Determine Threat Level:
    - High: More than one major or minor version behind.
    - Warn: One patch version behind.
    - Info: Up-to-date.
- Output Results: Structure the results with nested sub-messages.
- Register Task: Ensure the task is registered under the appropriate categories.
"""

import requests
from kubernetes import client, config
from kubesleuth.audit.registry import register_category
from packaging.version import Version

@register_category('General', 'Versions')  # Register the class with categories
class CheckVersions:

    def __init__(self):
        self.latest_stable_version = self.get_latest_stable_version()
        self.current_versions = self.get_current_versions()
        self.categories = self.__class__.categories

    def get_latest_stable_version(self) -> Version:
        stable_version_url = "https://storage.googleapis.com/kubernetes-release/release/stable.txt"
        response = requests.get(stable_version_url)
        response.raise_for_status()
        latest_stable_version = response.text.strip()
        return Version(latest_stable_version)
    
    def get_current_versions(self) -> dict:
        config.load_kube_config()
        api_instance = client.VersionApi()
        current_version = api_instance.get_code().git_version
        return {
            "kube-apiserver": Version(current_version),
            "kubelet": Version(current_version),
        }
    
    def compare_versions(self) -> list:
      results = []
      for component_name, current_version in self.current_versions.items():
          if (current_version.major != self.latest_stable_version.major or
              current_version.minor != self.latest_stable_version.minor):
              threat_level = "high"
              message = f"Version is out of date. Current version: {current_version}, Latest stable version: {self.latest_stable_version}"
          elif current_version.micro != self.latest_stable_version.micro:
              threat_level = "warn"
              message = f"Version is out of date. Current version: {current_version}, Latest stable version: {self.latest_stable_version}"
          else:
              threat_level = "info"
              message = f"Version is up to date with version {current_version}"

          # Create result entry
          result = {
              'threat': threat_level,
              'categories': list(self.categories),  # Pull categories from class attribute
              'resource_id': component_name,
              'message': message
          }
          results.append(result)
      return results
    
    def run(self) -> list:
        return self.compare_versions()
