# Implementation Plan
# - Load Kubernetes Configuration
# - Retrieve Resources in Default Namespace
# - Retrieve All Resources Across Namespaces
# - Calculate Percentage of Resources in Default Namespace
# - Determine Threat Level for Individual Resources:
#   - Warn: Individual resources in the default namespace.
# - Determine Threat Level for Overall Task:
#   - Critical: More than 30% of total resources in the default namespace.
# - Output Results with Nested Sub-Messages
# - Register Task

import logging
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubesleuth.audit.registry import register_category

logger = logging.getLogger(__name__)

@register_category('Configuration', 'Security', 'General')
class NamespaceIsolation:
    
    def __init__(self):
        self.categories = self.__class__.categories  # Initialize categories from class attribute
        config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def get_default_namespace_resources(self) -> dict:
        resources = {
            'pods': [],
            'services': [],
            'configmaps': [],
            'secrets': [],
            'persistentvolumeclaims': []
        }

        try:
            resources['pods'] = self.v1.list_namespaced_pod('default').items
            resources['services'] = self.v1.list_namespaced_service('default').items
            resources['configmaps'] = self.v1.list_namespaced_config_map('default').items
            resources['secrets'] = self.v1.list_namespaced_secret('default').items
            resources['persistentvolumeclaims'] = self.v1.list_namespaced_persistent_volume_claim('default').items
        except ApiException as e:
            logger.error(f"Error fetching resources from default namespace: {e}")

        return resources

    def get_all_resources(self) -> dict:
        all_resources = {
            'pods': [],
            'services': [],
            'configmaps': [],
            'secrets': [],
            'persistentvolumeclaims': []
        }

        try:
            namespaces = self.v1.list_namespace().items
            for ns in namespaces:
                all_resources['pods'].extend(self.v1.list_namespaced_pod(ns.metadata.name).items)
                all_resources['services'].extend(self.v1.list_namespaced_service(ns.metadata.name).items)
                all_resources['configmaps'].extend(self.v1.list_namespaced_config_map(ns.metadata.name).items)
                all_resources['secrets'].extend(self.v1.list_namespaced_secret(ns.metadata.name).items)
                all_resources['persistentvolumeclaims'].extend(self.v1.list_namespaced_persistent_volume_claim(ns.metadata.name).items)
        except ApiException as e:
            logger.error(f"Error fetching resources across namespaces: {e}")

        return all_resources

    def check_namespace_isolation(self) -> dict:
        default_namespace_resources = self.get_default_namespace_resources()
        all_resources = self.get_all_resources()

        total_resources = sum(len(resources) for resources in all_resources.values())
        default_resources = sum(len(resources) for resources in default_namespace_resources.values())

        percentage_default = (default_resources / total_resources) * 100 if total_resources > 0 else 0
        overall_threat_level = "info" if percentage_default <= 30 else "critical"

        results = {
            'threat': overall_threat_level,
            'categories': self.categories,
            'resource_id': 'namespace_isolation',
            'message': f"{percentage_default:.2f}% of resources are in the default namespace.",
            'sub_messages': []
        }

        for resource_type, resources in default_namespace_resources.items():
            for resource in resources:
                sub_message = {
                    'threat': "warn",
                    'resource_id': f"{resource_type}/{resource.metadata.name}",
                    'message': f"{resource_type.capitalize()} {resource.metadata.name} is in the default namespace"
                }
                results['sub_messages'].append(sub_message)

        return results

    def run(self) -> dict:
        return self.check_namespace_isolation()
