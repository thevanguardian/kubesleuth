import os
import logging
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubesleuth.audit.registry import register_category

logger = logging.getLogger(__name__)

@register_category('Security', 'NamespaceIsolation', 'CIS_Benchmark', 'Configuration')
class NamespaceIsolation:
    
    def __init__(self):
        self.categories = self.__class__.categories  # Initialize categories from class attribute
        config.load_kube_config()
        self.v1_core = client.CoreV1Api()
        self.v1_apps = client.AppsV1Api()
        self.resource_id = os.path.splitext(os.path.basename(__file__))[0]  # Set resource_id to filename sans extension

    def get_namespaced_resources(self) -> dict:
        """
        Retrieves all namespaced resources (pods, services, configmaps, secrets, PVCs).
        :return: Dictionary of namespaced resources.
        """
        resources = {
            'pods': [],
            'services': [],
            'configmaps': [],
            'secrets': [],
            'persistent_volume_claims': []
        }
        try:
            namespaces = self.v1_core.list_namespace().items
            for ns in namespaces:
                ns_name = ns.metadata.name
                resources['pods'].extend(self.v1_core.list_namespaced_pod(ns_name).items)
                resources['services'].extend(self.v1_core.list_namespaced_service(ns_name).items)
                resources['configmaps'].extend(self.v1_core.list_namespaced_config_map(ns_name).items)
                resources['secrets'].extend(self.v1_core.list_namespaced_secret(ns_name).items)
                resources['persistent_volume_claims'].extend(self.v1_core.list_namespaced_persistent_volume_claim(ns_name).items)
        except ApiException as e:
            logger.error(f"Error fetching namespaced resources: {e}")
        return resources

    def check_namespace_isolation(self) -> dict:
        """
        Checks namespace isolation for compliance based on CIS Benchmarks.
        :return: Dictionary of compliance results with threat levels and sub-messages.
        """
        resources = self.get_namespaced_resources()
        total_resources = sum(len(res_list) for res_list in resources.values())
        default_namespace_resources = sum(len([res for res in res_list if res.metadata.namespace == 'default']) for res_list in resources.values())
        default_namespace_percentage = (default_namespace_resources / total_resources) * 100 if total_resources > 0 else 0

        results = {
            'threat': 'info',
            'categories': self.categories,
            'resource_id': self.resource_id,
            'message': 'Kubernetes namespace isolation compliance scan.',
            'sub_messages': []
        }

        def add_sub_message(threat, resource_id, message):
            sub_message = {
                'threat': threat,
                'resource_id': resource_id,
                'message': message
            }
            results['sub_messages'].append(sub_message)
            if threat == 'critical' and results['threat'] != 'critical':
                results['threat'] = 'critical'
            elif threat == 'warn' and results['threat'] not in ['critical', 'warn']:
                results['threat'] = 'warn'

        for res_type, res_list in resources.items():
            for res in res_list:
                if res.metadata.namespace == 'default':
                    add_sub_message('warn', f"{res_type}/{res.metadata.name}", f"Resource {res.metadata.name} of type {res_type} is in the default namespace.")

        if default_namespace_percentage > 30:
            results['threat'] = 'critical'
            results['message'] += f" {default_namespace_percentage:.2f}% of resources are in the default namespace, exceeding the 30% threshold."

        return results

    def run(self) -> dict:
        """
        Runs the namespace isolation compliance check task.
        :return: Dictionary of results from the namespace isolation compliance check.
        """
        return self.check_namespace_isolation()
