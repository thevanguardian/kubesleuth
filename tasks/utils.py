from kubernetes import config

def append_issue(issues, issue, severity, namespace=None, name=None, pod=None):
    issues.append({
        "issue": issue,
        "severity": severity,
        "namespace": namespace,
        "name": name,
        "pod": pod
    })

def load_kube_config(kubeconfig=None, context=None):
    if kubeconfig and context:
        config.load_kube_config(config_file=kubeconfig, context=context)
    elif kubeconfig:
        config.load_kube_config(config_file=kubeconfig)
    elif context:
        config.load_kube_config(context=context)
    else:
        config.load_kube_config()
