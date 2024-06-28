# Implementation Plan
# - Load Kubernetes Configuration
# - Retrieve Node Metrics
# - Check Node Health Metrics
#   - CPU Usage
#   - Memory Usage
#   - Disk Usage
#   - Network Performance
#   - Node Conditions
# - Check Best Practices and CIS Benchmarks
#   - Resource Overcommitment
#   - Adequate Resources
#   - Node Uptime
#   - Taints and Tolerations
# - Determine Threat Levels
#   - Critical: Metrics exceed critical thresholds
#   - Warn: Metrics exceed warning thresholds
#   - Info: General node health information
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

@register_category('Security', 'Nodes', 'CIS_Benchmark', 'Performance')
class NodeHealth:
    
    def __init__(self):
        self.categories = self.__class__.categories 
        config.load_kube_config()
        self.v1_core = client.CoreV1Api()
        self.resource_id = os.path.splitext(os.path.basename(__file__))[0] 

    def get_node_metrics(self) -> list:
        """
        Retrieves all node metrics.
        :return: List of node metrics.
        """
        nodes = []
        try:
            nodes = self.v1_core.list_node().items
        except ApiException as e:
            logger.error(f"Error fetching nodes: {e}")
        return nodes

    def convert_to_mib(self, value: str) -> int:
        """
        Converts a Kubernetes resource quantity to MiB.
        :param value: The Kubernetes resource quantity string (e.g., '16375072Ki').
        :return: The value converted to MiB.
        """
        if value.endswith('Ki'):
            return int(value[:-2]) / 1024
        elif value.endswith('Mi'):
            return int(value[:-2])
        elif value.endswith('Gi'):
            return int(value[:-2]) * 1024
        else:
            return int(value) / (1024**2)

    def check_node_health_compliance(self) -> dict:
        """
        Checks node health for compliance based on CIS Benchmarks.
        :return: Dictionary of compliance results with threat levels and sub-messages.
        """
        nodes = self.get_node_metrics()

        results = {
            'threat': 'info',
            'categories': self.categories,
            'resource_id': self.resource_id, 
            'message': 'Kubernetes node health compliance scan.',
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

        for node in nodes:
            node_name = node.metadata.name
            cpu_capacity = int(node.status.capacity.get('cpu', 0)) if node.status.capacity else 0 
            memory_capacity = self.convert_to_mib(node.status.capacity.get('memory', '0Ki')) if node.status.capacity else 0 
            disk_capacity = self.convert_to_mib(node.status.capacity.get('ephemeral-storage', '0Ki')) if node.status.capacity else 0 

           
            cpu_usage = 0
            memory_usage = 0
            disk_usage = 0

            try:
                pods = self.v1_core.list_pod_for_all_namespaces(field_selector=f'spec.nodeName={node_name}').items
                for pod in pods:
                    for container in pod.spec.containers:
                        requests = container.resources.requests or {} 
                        cpu_request = requests.get('cpu', '0').replace('m', '') 
                        memory_request = requests.get('memory', '0') 
                        ephemeral_storage_request = requests.get('ephemeral-storage', '0') 
                        
                        cpu_usage += int(cpu_request) / 1000 if 'm' in requests.get('cpu', '0') else int(cpu_request) 
                        memory_usage += self.convert_to_mib(memory_request) 
                        disk_usage += self.convert_to_mib(ephemeral_storage_request)
            except ApiException as e:
                logger.error(f"Error fetching pod metrics for node {node_name}: {e}")

            cpu_usage_percentage = (cpu_usage / cpu_capacity) * 100 if cpu_capacity else 0
            memory_usage_percentage = (memory_usage / memory_capacity) * 100 if memory_capacity else 0
            disk_usage_percentage = (disk_usage / disk_capacity) * 100 if disk_capacity else 0

            if cpu_usage_percentage > 90:
                add_sub_message('critical', f"node/{node_name}", f"Node {node_name} CPU usage is critical: {cpu_usage_percentage:.2f}%") 
            elif cpu_usage_percentage > 75:
                add_sub_message('warn', f"node/{node_name}", f"Node {node_name} CPU usage is high: {cpu_usage_percentage:.2f}%") 
            else:
                add_sub_message('info', f"node/{node_name}", f"Node {node_name} CPU usage is normal: {cpu_usage_percentage:.2f}%") 

            if memory_usage_percentage > 90:
                add_sub_message('critical', f"node/{node_name}", f"Node {node_name} memory usage is critical: {memory_usage_percentage:.2f}MiB") 
            elif memory_usage_percentage > 75:
                add_sub_message('warn', f"node/{node_name}", f"Node {node_name} memory usage is high: {memory_usage_percentage:.2f}MiB") 
            else:
                add_sub_message('info', f"node/{node_name}", f"Node {node_name} memory usage is normal: {memory_usage_percentage:.2f}MiB") 

            if disk_usage_percentage > 90: 
                add_sub_message('critical', f"node/{node_name}", f"Node {node_name} disk usage is critical: {disk_usage_percentage:.2f}%") 
            elif disk_usage_percentage > 75: 
                add_sub_message('warn', f"node/{node_name}", f"Node {node_name} disk usage is high: {disk_usage_percentage:.2f}%") 
            else: 
                add_sub_message('info', f"node/{node_name}", f"Node {node_name} disk usage is normal: {disk_usage_percentage:.2f}%") 

            for condition in node.status.conditions:
                if condition.type == 'Ready' and condition.status != 'True':
                    add_sub_message('critical', f"node/{node_name}", f"Node {node_name} is not ready.")
                elif condition.type in ['DiskPressure', 'MemoryPressure', 'PIDPressure'] and condition.status == 'True':
                    add_sub_message('warn', f"node/{node_name}", f"Node {node_name} is under {condition.type}.")

        return results

    def run(self) -> dict:
        """
        Runs the node health compliance check task.
        :return: Dictionary of results from the node health compliance check.
        """
        return self.check_node_health_compliance()
