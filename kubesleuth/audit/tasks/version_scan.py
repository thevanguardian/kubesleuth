# Implementation Plan
# - Load Kubernetes Configuration
# - Retrieve Component Versions
# - Fetch Latest Stable Version
# - Compare Versions
# - Determine Threat Level:
#   - Critical: More than one major or minor version behind.
#   - Warn: One patch version behind.
#   - Info: Up-to-date.
# - Output Results
# - Register Task

import logging
import requests
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubesleuth.audit.registry import register_category
from packaging.version import Version

logger = logging.getLogger(__name__)

@register_category('Configuration', 'General')
class CheckVersions:

    def __init__(self):
        self.categories = self.__class__.categories  # Initialize categories from class attribute
        config.load_kube_config()
        self.v1 = client.VersionApi()
        self.latest_stable_version = self.get_latest_stable_version()
        self.current_versions = self.get_current_versions()

    def get_latest_stable_version(self) -> Version:
        stable_version_url = "https://storage.googleapis.com/kubernetes-release/release/stable.txt"
        try:
            response = requests.get(stable_version_url)
            response.raise_for_status()
            latest_stable_version = response.text.strip()
            return Version(latest_stable_version)
        except requests.RequestException as e:
            logger.error(f"Error fetching latest stable version: {e}")
            return Version("0.0.0")  # Fallback to a dummy version

    def get_current_versions(self) -> dict:
        try:
            current_version = self.v1.get_code().git_version
            return {
                "kube-apiserver": Version(current_version),  # CIS Benchmark 1.1.1
                "kubelet": Version(current_version),         # CIS Benchmark 2.1.1
            }
        except ApiException as e:
            logger.error(f"Error fetching current versions: {e}")
            return {
                "kube-apiserver": Version("0.0.0"),
                "kubelet": Version("0.0.0"),
            }  # Fallback to dummy versions

    def compare_versions(self) -> dict:
        results = {
            'threat': 'info',
            'categories': self.categories,
            'resource_id': 'version_scan',
            'message': 'Kubernetes component version comparison.',
            'sub_messages': []
        }

        for component_name, current_version in self.current_versions.items():
            if (current_version.major != self.latest_stable_version.major or
                current_version.minor != self.latest_stable_version.minor):
                threat_level = "critical"
            elif current_version.micro != self.latest_stable_version.micro:
                threat_level = "warn"
            else:
                threat_level = "info"

            sub_message = {
                'threat': threat_level,
                'resource_id': f"{component_name}",
                'message': f"{component_name} version {current_version} vs stable {self.latest_stable_version}"
            }
            results['sub_messages'].append(sub_message)

            # Update main threat level if any sub-message has a higher threat level
            if threat_level == "critical":
                results['threat'] = "critical"
            elif threat_level == "warn" and results['threat'] != "critical":
                results['threat'] = "warn"

        return results

    def run(self) -> dict:
        return self.compare_versions()
