from typing import List, Dict

def append_issue(issues: List[Dict[str, str]], name: str, namespace: str, fault: str, threat: str):
    issue = {
        "name": name,
        "namespace": namespace,
        "fault": fault,
        "threat": threat
    }
    issues.append(issue)

def load_kube_config(kubeconfig=None, context=None):
    from kubernetes import config
    if kubeconfig and context:
        config.load_kube_config(config_file=kubeconfig, context=context)
    elif kubeconfig:
        config.load_kube_config(config_file=kubeconfig)
    elif context:
        config.load_kube_config(context=context)
    else:
        config.load_kube_config()
