from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, Any
from .utils import append_issue

def check_namespace_isolation() -> Dict[str, Any]:
    issues = []
    config.load_kube_config()
    core_v1 = client.CoreV1Api()
    rbac_v1 = client.RbacAuthorizationV1Api()
    networking_v1 = client.NetworkingV1Api()

    try:
        namespaces = core_v1.list_namespace().items
        for namespace in namespaces:
            namespace_name = namespace.metadata.name
            
            # Info issues for all namespaces and their contents
            pods = core_v1.list_namespaced_pod(namespace_name).items
            for pod in pods:
                append_issue(issues, f"pod/{pod.metadata.name}", namespace_name, "Pod found in namespace.", "Info")

            services = core_v1.list_namespaced_service(namespace_name).items
            for service in services:
                append_issue(issues, f"service/{service.metadata.name}", namespace_name, "Service found in namespace.", "Info")

            configmaps = core_v1.list_namespaced_config_map(namespace_name).items
            for configmap in configmaps:
                append_issue(issues, f"configmap/{configmap.metadata.name}", namespace_name, "ConfigMap found in namespace.", "Info")

            secrets = core_v1.list_namespaced_secret(namespace_name).items
            for secret in secrets:
                append_issue(issues, f"secret/{secret.metadata.name}", namespace_name, "Secret found in namespace.", "Info")

            pvcs = core_v1.list_namespaced_persistent_volume_claim(namespace_name).items
            for pvc in pvcs:
                append_issue(issues, f"pvc/{pvc.metadata.name}", namespace_name, "PersistentVolumeClaim found in namespace.", "Info")

            # Check for resources in the default namespace
            if namespace_name == "default":
                if pods:
                    for pod in pods:
                        append_issue(issues, f"pod/{pod.metadata.name}", "default", "Pod is in the default namespace.", "High")
                if services:
                    for service in services:
                        append_issue(issues, f"service/{service.metadata.name}", "default", "Service is in the default namespace.", "High")
                if configmaps:
                    for configmap in configmaps:
                        append_issue(issues, f"configmap/{configmap.metadata.name}", "default", "ConfigMap is in the default namespace.", "High")
                if secrets:
                    for secret in secrets:
                        append_issue(issues, f"secret/{secret.metadata.name}", "default", "Secret is in the default namespace.", "High")
                if pvcs:
                    for pvc in pvcs:
                        append_issue(issues, f"pvc/{pvc.metadata.name}", "default", "PersistentVolumeClaim is in the default namespace.", "High")

            # Check for network policies in each namespace
            netpols = networking_v1.list_namespaced_network_policy(namespace_name).items
            if not netpols:
                append_issue(issues, f"netpol/none", namespace_name, "No network policies are in place.", "High")

            # Check for ResourceQuotas in each namespace
            resource_quotas = core_v1.list_namespaced_resource_quota(namespace_name).items
            if not resource_quotas:
                append_issue(issues, f"resourcequota/none", namespace_name, "No resource quotas are in place.", "Medium")

            # Check for LimitRanges in each namespace
            limit_ranges = core_v1.list_namespaced_limit_range(namespace_name).items
            if not limit_ranges:
                append_issue(issues, f"limitrange/none", namespace_name, "No limit ranges are in place.", "Medium")

            # Check for RBAC policies
            role_bindings = rbac_v1.list_namespaced_role_binding(namespace_name).items
            if not role_bindings:
                append_issue(issues, f"rolebinding/none", namespace_name, "No role bindings are in place.", "Medium")

        return {"issues": issues}
    except ApiException as e:
        print(f"Exception when checking namespace isolation: {e}")
        return {"issues": issues}
    finally:
        core_v1.api_client.close()
        rbac_v1.api_client.close()
        networking_v1.api_client.close()

# Example usage for debugging
if __name__ == "__main__":
    result = check_namespace_isolation()
    print(result)
