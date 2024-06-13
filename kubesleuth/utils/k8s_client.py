import logging
from typing import Optional
from kubernetes import client, config
from kubernetes.config import ConfigException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_k8s_config(kubeconfig: Optional[str] = None, context: Optional[str] = None) -> client.ApiClient:
    try:
        # Load configuration from kubeconfig file or default location
        if kubeconfig:
            logger.info("Loading kubeconfig from file: %s", kubeconfig)
            config.load_kube_config(config_file=kubeconfig, context=context)
        else:
            logger.info("Loading kubeconfig from default location")
            config.load_kube_config(context=context)
        logger.info("Kubernetes configuration loaded successfully")
    except ConfigException as e:
        logger.warning("Failed to load kubeconfig: %s. Attempting in-cluster configuration.", e)
        try:
            # Attempt to load in-cluster configuration
            config.load_incluster_config()
            logger.info("In-cluster Kubernetes configuration loaded successfully")
        except ConfigException as e:
            # Raise error if both configurations fail
            logger.error("Could not configure Kubernetes connection: %s", e)
            raise RuntimeError("Could not configure Kubernetes connection: {}".format(e))

    # Return Kubernetes API client
    return client.ApiClient()
