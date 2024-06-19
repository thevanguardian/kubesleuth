"""
Implementation Plan for Namespace Isolation Task
- Load Kubernetes Configuration: Load the Kubernetes configuration to access the cluster.
- Retrieve Resources in the Default Namespace: Fetch resources specifically in the 'default' namespace.
- Calculate Percentage of Resources in Default Namespace: Calculate the percentage of resources in the default namespace relative to the total number of resources.
- Determine Threat Level:
    - High: More than 30% of resources are in the default namespace.
    - Warn: Between 0% and 30% of resources are in the default namespace.
    - Info: 0% of resources are in the default namespace.
- Output Results: Verbosely output the checked items and their statuses.
- Register Task: Ensure the task is registered under the appropriate categories.
"""

import logging
from kubernetes import client, config
from kubesleuth.audit.registry import register_category

logger = logging.getLogger(__name__)

@register_category('Configuration', 'Security', 'General')
class NamespaceIsolation:
    
    def __init__(self):
        self.categories = list(self.__class__.categories)  # Initialize categories from class attribute as a list
        config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def get_default_namespace_resources(self):
        """
        Retrieves all resources in the 'default' namespace.
        :return: List of resources in the default namespace.
        """
        resources = self.v1.list_namespaced_pod('default').items  # Example resource type: pods
        return resources

    def get_all_resources(self):
        """
        Retrieves all resources across all namespaces.
        :return: List of all resources.
        """
        all_resources = []
        namespaces = self.v1.list_namespace().items
        for ns in namespaces:
            resources = self.v1.list_namespaced_pod(ns.metadata.name).items  # Example resource type: pods
            all_resources.extend(resources)
        return all_resources

    def check_namespace_isolation(self) -> dict:
        """
        Checks for namespace isolation compliance.
        Satisfies CIS Benchmark for ensuring proper namespace usage.
        :return: Dictionary of comparison results with threat levels and sub-messages.
        """
        default_namespace_resources = self.get_default_namespace_resources()
        all_resources = self.get_all_resources()

        total_resources = len(all_resources)
        default_resources = len(default_namespace_resources)

        percentage_default = (default_resources / total_resources) * 100 if total_resources > 0 else 0
        if percentage_default > 30:
            threat_level = "high"
        elif 0 < percentage_default <= 30:
            threat_level = "warn"
        else:
            threat_level = "info"

        results = {
            'threat': threat_level,
            'categories': self.categories,
            'resource_id': 'namespace_isolation',
            'message': f"{percentage_default:.2f}% of resources are in the default namespace.",
            'sub_messages': []
        }

        for resource in default_namespace_resources:
            sub_message = {
                'threat': threat_level,
                'resource_id': f"{resource.metadata.name}",
                'message': f"Resource {resource.metadata.name} is in the default namespace"
            }
            results['sub_messages'].append(sub_message)

        return results

    def run(self) -> dict:
        """
        Runs the namespace isolation check task.
        :return: Dictionary of results from the namespace isolation check.
        """
        return self.check_namespace_isolation()
