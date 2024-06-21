import os
import logging
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubesleuth.audit.registry import register_category

logger = logging.getLogger(__name__)

@register_category('Security', 'RBAC', 'CIS_Benchmark', 'Configuration')
class CustomRolesScan:
    
    def __init__(self):
        self.categories = self.__class__.categories  # Initialize categories from class attribute
        config.load_kube_config()
        self.v1_rbac = client.RbacAuthorizationV1Api()
        self.v1_core = client.CoreV1Api()
        self.resource_id = os.path.splitext(os.path.basename(__file__))[0]  # Set resource_id to filename sans extension

    def get_custom_roles(self) -> list:
        """
        Retrieves all custom roles and cluster roles.
        :return: List of custom roles and cluster roles.
        """
        roles = []
        try:
            roles.extend(self.v1_rbac.list_cluster_role().items)
            namespaces = self.v1_core.list_namespace().items
            for ns in namespaces:
                roles.extend(self.v1_rbac.list_namespaced_role(ns.metadata.name).items)
        except ApiException as e:
            logger.error(f"Error fetching roles: {e}")
        return roles

    def check_custom_roles_compliance(self) -> dict:
        """
        Checks custom roles for compliance based on CIS Benchmarks.
        :return: Dictionary of compliance results with threat levels and sub-messages.
        """
        roles = self.get_custom_roles()

        results = {
            'threat': 'info',
            'categories': self.categories,
            'resource_id': self.resource_id,
            'message': 'Kubernetes custom roles compliance scan.',
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

        # Check roles for wildcard permissions
        for role in roles:
            for rule in role.rules:
                if ('*' in rule.verbs if rule.verbs else False) or \
                   ('*' in rule.resources if rule.resources else False) or \
                   ('*' in rule.api_groups if rule.api_groups else False):
                    add_sub_message('critical', f"role/{role.metadata.name}", f"Role {role.metadata.name} has wildcard permissions.")
        
        # More checks for least privilege, separation of duties, and namespace scoping
        for role in roles:
            if 'system:' not in role.metadata.name:
                add_sub_message('info', f"role/{role.metadata.name}", f"Custom role {role.metadata.name} found.")
                for rule in role.rules:
                    if not rule.resources or not rule.verbs or not rule.api_groups:
                        add_sub_message('warn', f"role/{role.metadata.name}", f"Role {role.metadata.name} does not adhere to least privilege principles.")
                    if rule.resources and 'namespaces' not in rule.resources:
                        add_sub_message('warn', f"role/{role.metadata.name}", f"Role {role.metadata.name} is not namespace-scoped.")
        
        return results

    def run(self) -> dict:
        """
        Runs the custom roles compliance check task.
        :return: Dictionary of results from the custom roles compliance check.
        """
        return self.check_custom_roles_compliance()
