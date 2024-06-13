import argparse
from kubesleuth.version import __version__
from kubesleuth.utils.k8s_client import load_k8s_config
import kubesleuth.audit.tasks  # Ensure tasks are dynamically imported and registered
from kubesleuth.audit.registry import get_tasks_by_category, get_available_categories
from kubernetes.client import ApiClient, CoreV1Api
from kubernetes.client.rest import ApiException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_k8s_connectivity(api_client: ApiClient) -> bool:
    try:
        v1 = CoreV1Api(api_client)
        v1.get_api_resources()
        logger.info("Kubernetes connectivity verified")
        return True
    except ApiException as e:
        logger.error("Failed to verify Kubernetes connectivity: %s", e)
        return False

def main():
    parser = argparse.ArgumentParser(description="Kubernetes Configuration Audit by KubeSleuth")
    parser.add_argument("--output", choices=["json", "markdown", "yaml"], default="json", help="Output format (json, markdown, or yaml)")
    parser.add_argument("--kubeconfig", help="Path to the kubeconfig file", default=None)
    parser.add_argument("--context", help="Kubernetes context to use", default=None)
    parser.add_argument("--level", choices=["high", "medium", "low", "info", "debug"], default="all", help="Assessment level to display")
    parser.add_argument("--version", action="version", version=f"{__version__}")

    # Dynamically get the list of available categories
    available_categories = get_available_categories()
    parser.add_argument("--category", choices=available_categories, help="Category of tasks to run")

    args = parser.parse_args()

    # Load Kubernetes configuration
    k8s_client = load_k8s_config(kubeconfig=args.kubeconfig, context=args.context)

    # Verify Kubernetes connectivity
    if not verify_k8s_connectivity(k8s_client):
        logger.error("Unable to connect to Kubernetes cluster. Exiting.")
        exit(1)

    # Run tasks based on category
    if args.category:
        tasks = get_tasks_by_category(args.category)
        for task in tasks:
            task()

    # Placeholder for future functionality
    print(f"Output format: {args.output}")
    print(f"Kubeconfig path: {args.kubeconfig}")
    print(f"Kubernetes context: {args.context}")
    print(f"Assessment level: {args.level}")

if __name__ == "__main__":
    main()
