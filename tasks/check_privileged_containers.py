from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any, List
from .utils import append_issue

def check_privileged_containers() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    try:
        pods = core_v1.list_pod_for_all_namespaces().items
        for pod in pods:
            for container in pod.spec.containers:
                container_name = f"pod/{pod.metadata.name}/{container.name}"
                namespace = pod.metadata.namespace
                security_context = container.security_context

                # Generate Info issues for all containers
                append_issue(issues, container_name, namespace, "Container configuration found.", "Info")

                # Check if container is privileged
                if security_context and security_context.privileged:
                    append_issue(issues, container_name, namespace, "Container is running with privileged security context.", "High")

                # Check for read-only root filesystem
                if not security_context or not security_context.read_only_root_filesystem:
                    append_issue(issues, container_name, namespace, "Container does not have a read-only root filesystem.", "Medium")

                # Check for unnecessary capabilities
                if security_context and security_context.capabilities and security_context.capabilities.drop:
                    if 'ALL' not in security_context.capabilities.drop:
                        append_issue(issues, container_name, namespace, "Container does not drop all unnecessary capabilities.", "Medium")

                # Check for host network mode
                if pod.spec.host_network:
                    append_issue(issues, container_name, namespace, "Pod is using the host network mode.", "Medium")

                # Check if container runs as root user
                if not security_context or not security_context.run_as_user or security_context.run_as_user == 0:
                    append_issue(issues, container_name, namespace, "Container is running as the root user.", "Medium")

                # Check for host IPC mode
                if pod.spec.host_ipc:
                    append_issue(issues, container_name, namespace, "Pod is using the host IPC mode.", "Medium")

                # Check for host PID mode
                if pod.spec.host_pid:
                    append_issue(issues, container_name, namespace, "Pod is using the host PID mode.", "Medium")

        return {"issues": issues}
    except ApiException as e:
        print(f"Exception when checking privileged containers: {e}")
        return {"issues": issues}
    finally:
        core_v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_privileged_containers()
    print(result)
