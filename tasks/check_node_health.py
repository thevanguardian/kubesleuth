from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue

def check_node_health() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    try:
        nodes = core_v1.list_node().items
        for node in nodes:
            node_name = node.metadata.name

            # Generate Info issue for the node
            append_issue(issues, f"node/{node_name}", "default", f"Node configuration found.", "Info")

            # Check node conditions
            for condition in node.status.conditions:
                if condition.type == "Ready" and condition.status != "True":
                    append_issue(issues, f"node/{node_name}", "default", "Node is not in Ready state.", "High")
                if condition.type == "DiskPressure" and condition.status == "True":
                    append_issue(issues, f"node/{node_name}", "default", "Node has DiskPressure.", "Medium")
                if condition.type == "MemoryPressure" and condition.status == "True":
                    append_issue(issues, f"node/{node_name}", "default", "Node has MemoryPressure.", "Medium")
                if condition.type == "PIDPressure" and condition.status == "True":
                    append_issue(issues, f"node/{node_name}", "default", "Node has PIDPressure.", "Medium")
                if condition.type == "NetworkUnavailable" and condition.status == "True":
                    append_issue(issues, f"node/{node_name}", "default", "Node has NetworkUnavailable.", "Medium")

            # Check node resource allocations
            allocatable = node.status.allocatable
            capacity = node.status.capacity
            if allocatable['cpu'] < '2':
                append_issue(issues, f"node/{node_name}", "default", "Node has less than 2 CPUs allocatable.", "Medium")
            if allocatable['memory'] < '8Gi':
                append_issue(issues, f"node/{node_name}", "default", "Node has less than 8Gi of memory allocatable.", "Medium")

            # Check node taints
            for taint in node.spec.taints:
                if taint.effect in ["NoSchedule", "NoExecute"]:
                    append_issue(issues, f"node/{node_name}", "default", f"Node has taint {taint.key} with effect {taint.effect}.", "Medium")

        return {"issues": issues}
    except ApiException as e:
        print(f"Exception when checking node health: {e}")
        return {"issues": issues}
    finally:
        core_v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_node_health()
    print(result)
