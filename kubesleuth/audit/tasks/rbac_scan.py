# Implementation Plan
# - Load Kubernetes Configuration
# - Retrieve All Roles and ClusterRoles
# - Retrieve All RoleBindings and ClusterRoleBindings
# - Check for CIS Benchmark RBAC Items
#   - Ensure no wildcard '*' permissions
#   - Ensure least privilege principles
#   - Ensure no use of the 'system:masters' group
#   - Ensure default service accounts are not used for deployments
#   - Ensure ServiceAccount Tokens are only accessible where needed
# - Determine Threat Levels
#   - Critical: Violations that pose high security risks
#   - Warn: Potential issues that should be reviewed
#   - Info: Compliance information
# - Output Results with Nested Sub-Messages
# - Register Task

import os
import logging
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubesleuth.audit.registry import register_category

logger = logging.getLogger(__name__)

@register_category('Security', 'RBAC', 'CIS_Benchmark', 'User')
class RBACScan:
    
    def __init__(self):
        self.categories = self.__class__.categories  # Initialize categories from class attribute
        config.load_kube_config()
        self.v1_rbac = client.RbacAuthorizationV1Api()
        self.v1_core = client.CoreV1Api()
        self.v1_apps = client.AppsV1Api()
        self.resource_id = os.path.splitext(os.path.basename(__file__))[0]  # Set resource_id to filename sans extension

    def get_roles(self) -> list:
        """
        Retrieves all roles and cluster roles.
        :return: List of roles and cluster roles.
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

    def get_role_bindings(self) -> list:
        """
        Retrieves all role bindings and cluster role bindings.
        :return: List of role bindings and cluster role bindings.
        """
        bindings = []
        try:
            bindings.extend(self.v1_rbac.list_cluster_role_binding().items)
            namespaces = self.v1_core.list_namespace().items
            for ns in namespaces:
                bindings.extend(self.v1_rbac.list_namespaced_role_binding(ns.metadata.name).items)
        except ApiException as e:
            logger.error(f"Error fetching role bindings: {e}")
        return bindings

    def get_deployments_using_default_sa(self) -> list:
        """
        Retrieves all deployments using the default service account.
        :return: List of deployments using the default service account.
        """
        deployments = []
        try:
            namespaces = self.v1_core.list_namespace().items
            for ns in namespaces:
                deployments_in_ns = self.v1_apps.list_namespaced_deployment(ns.metadata.name).items
                for deployment in deployments_in_ns:
                    if deployment.spec.template.spec.service_account_name == 'default':
                        deployments.append(deployment)
        except ApiException as e:
            logger.error(f"Error fetching deployments: {e}")
        return deployments

    def check_rbac_compliance(self) -> dict:
        """
        Checks for RBAC compliance based on CIS Benchmarks.
        :return: Dictionary of compliance results with threat levels and sub-messages.
        """
        roles = self.get_roles()
        bindings = self.get_role_bindings()
        deployments = self.get_deployments_using_default_sa()

        results = {
            'threat': 'info',
            'categories': self.categories,
            'resource_id': self.resource_id,
            'message': 'Kubernetes RBAC compliance scan.',
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
        
        # Check for least privilege
        for binding in bindings:
          if binding.subjects:
            for subject in binding.subjects:
                if subject.kind == 'Group' and subject.name == 'system:masters':
                    add_sub_message('critical', f"binding/{binding.metadata.name}", f"Binding {binding.metadata.name} uses 'system:masters' group.")

        # Check deployments using default service account
        for deployment in deployments:
            add_sub_message('warn', f"deployment/{deployment.metadata.name}", f"Deployment {deployment.metadata.name} is using the default service account.")
        
        # More checks can be added here as needed

        return results

    def run(self) -> dict:
        """
        Runs the RBAC compliance check task.
        :return: Dictionary of results from the RBAC compliance check.
        """
        return self.check_rbac_compliance()
