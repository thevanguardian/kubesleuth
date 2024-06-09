"""
This module contains various utility functions for checking the security posture of a Kubernetes cluster.

The `check_rbac` function checks the RBAC (Role-Based Access Control) configuration of the cluster.
The `check_password_auth` function checks the password-based authentication configuration.
The `check_custom_roles` function checks for the presence of custom RBAC roles.
The `check_network_policies` function checks the network policies configured in the cluster.
The `check_namespace_isolation` function checks the namespace isolation configuration.
The `check_privileged_containers` function checks for the presence of privileged containers.

The `append_issue` function is a utility function for appending security issues to a list.
The `load_kube_config` function is a utility function for loading the Kubernetes configuration.
"""
from .check_rbac import check_rbac
from .check_password_auth import check_password_auth
from .check_custom_roles import check_custom_roles
from .check_network_policies import check_network_policies
from .check_namespace_isolation import check_namespace_isolation
from .check_privileged_containers import check_privileged_containers
from .utils import append_issue, load_kube_config

__all__ = [
    "check_rbac",
    "check_password_auth",
    "check_custom_roles",
    "check_network_policies",
    "check_namespace_isolation",
    "check_privileged_containers",
    "append_issue",
    "load_kube_config"
]
