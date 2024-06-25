# Implementation Plan
# - Load Kubernetes Configuration
# - Retrieve Network Policies
# - Check Network Policies for Compliance
#   - Namespace Isolation
#   - Policy Enforcement
#   - Ingress and Egress Rules
#   - Policies for Each Namespace
#   - Default Deny Policies
#   - CNI Plugins
# - Determine Threat Levels
#   - Critical: Missing/Misconfigured Policies
#   - Warn: Potential Issues
#   - Info: Compliance Information
# - Output Results
#   - Include Nested Sub-Messages
# - Set `resource_id` to Filename without Extension
# - Error Handling and Logging

import os
import logging
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubesleuth.audit.registry import register_category

logger = logging.getLogger(__name__)

@register_category('Security', 'NetworkPolicies', 'CIS_Benchmark', 'NamespaceIsolation', 'Configuration')
class NetworkPoliciesScan:
    
    def __init__(self):
        self.categories = self.__class__.categories  # Initialize categories from class attribute
        config.load_kube_config()
        self.v1_networking = client.NetworkingV1Api()
        self.v1_core = client.CoreV1Api()  # Use CoreV1Api for listing namespaces [Changed]
        self.resource_id = os.path.splitext(os.path.basename(__file__))[0]  # Set resource_id to filename sans extension [Changed]

    def get_network_policies(self) -> list:
        """
        Retrieves all network policies.
        :return: List of network policies.
        """
        policies = []
        try:
            namespaces = self.v1_core.list_namespace().items  # Use CoreV1Api for listing namespaces [Changed]
            for ns in namespaces:
                policies.extend(self.v1_networking.list_namespaced_network_policy(ns.metadata.name).items)
        except ApiException as e:
            logger.error(f"Error fetching network policies: {e}")
        return policies

    def check_network_policies_compliance(self) -> dict:
        """
        Checks network policies for compliance based on CIS Benchmarks.
        :return: Dictionary of compliance results with threat levels and sub-messages.
        """
        policies = self.get_network_policies()

        results = {
            'threat': 'info',
            'categories': self.categories,
            'resource_id': self.resource_id,  # Set resource_id dynamically [Changed]
            'message': 'Kubernetes network policies compliance scan.',
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

        for policy in policies:
            # Check if policy applies to namespace isolation
            if not policy.spec.pod_selector:
                add_sub_message('critical', f"networkpolicy/{policy.metadata.name}", f"Network policy {policy.metadata.name} does not have a pod selector.")

            # Check for ingress and egress rules
            if not policy.spec.ingress and not policy.spec.egress:
                add_sub_message('critical', f"networkpolicy/{policy.metadata.name}", f"Network policy {policy.metadata.name} does not have ingress or egress rules.")

            # Ensure policy enforcement
            if not policy.spec.policy_types:
                add_sub_message('warn', f"networkpolicy/{policy.metadata.name}", f"Network policy {policy.metadata.name} does not specify policy types (Ingress/Egress).")

            # Ensure default deny policy
            if not policy.spec.ingress:  # Check if ingress rules are present [Changed]
                add_sub_message('warn', f"networkpolicy/{policy.metadata.name}", f"Network policy {policy.metadata.name} does not have default deny ingress rules.")  # Check if egress rules are present [Changed]
            if not policy.spec.egress:  # Check if egress rules are present [Changed]
                add_sub_message('warn', f"networkpolicy/{policy.metadata.name}", f"Network policy {policy.metadata.name} does not have default deny egress rules.")  # Check if egress rules are present [Changed]

            # Compliance info
            add_sub_message('info', f"networkpolicy/{policy.metadata.name}", f"Network policy {policy.metadata.name} is in place and being checked.")

        return results

    def run(self) -> dict:
        """
        Runs the network policies compliance check task.
        :return: Dictionary of results from the network policies compliance check.
        """
        return self.check_network_policies_compliance()
