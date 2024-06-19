import argparse
from kubesleuth.version import __version__
from kubesleuth.utils.k8s_client import load_k8s_config
import kubesleuth.audit.tasks  # Ensure tasks are dynamically imported and registered
from kubesleuth.audit.registry import get_tasks_by_category, get_available_categories
import kubesleuth.outputs
from kubernetes.client import ApiClient, CoreV1Api
from kubernetes.client.rest import ApiException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_k8s_connectivity(api_client: ApiClient) -> bool:
    """
    Verify Kubernetes connectivity.

    :param api_client: Kubernetes API client
    :return: True if connectivity is verified, False otherwise
    """
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
    parser.add_argument("--output", choices=["json", "markdown", "yaml", "console"], default="console", help="Output format (json, markdown, yaml, or console)")
    parser.add_argument("--kubeconfig", help="Path to the kubeconfig file", default=None)
    parser.add_argument("--context", help="Kubernetes context to use", default=None)
    parser.add_argument("--version", action="version", version=f"{__version__}")
    parser.add_argument("--level", choices=["high", "medium", "low", "info", "debug"], default="all", help="Assessment level to display")

    # Dynamically get the list of available categories and threats
    available_categories = get_available_categories()
    parser.add_argument("--category", choices=available_categories, default="General", help="Category of tasks to run")
    args = parser.parse_args()

    # Load Kubernetes configuration
    k8s_client = load_k8s_config(kubeconfig=args.kubeconfig, context=args.context)

    # Verify Kubernetes connectivity
    if not verify_k8s_connectivity(k8s_client):
        logger.error("Unable to connect to Kubernetes cluster. Exiting.")
        exit(1)

    # Placeholder for assessment results
    assessment_results = []

    # Collect unique tasks to avoid duplicates
    tasks_to_run = set()

    # Run tasks based on category
    if args.category:
        tasks = get_tasks_by_category(args.category)
        tasks_to_run.update(tasks)

    # Execute unique tasks
    for task in tasks_to_run:
        if isinstance(task, type):  # Check if the task is a class
            task_instance = task()  # Instantiate the class
            result = task_instance.run()  # Call the run method
        else:
            result = task()

        if result:
            assessment_results.extend(result)  # Extend the results list

    logger.info("Task %s completed successfully", task)
    logger.info("Assessment results: %s", assessment_results)
    # Output results
    if args.output == "console":
        from kubesleuth.outputs.console import output_console
        output_console(assessment_results)
    elif args.output == "json":
        from kubesleuth.outputs.json import output_json
        print(output_json(assessment_results))
    elif args.output == "yaml":
        from kubesleuth.outputs.yaml import output_yaml
        print(output_yaml(assessment_results))
    elif args.output == "markdown":
        from kubesleuth.outputs.markdown import output_markdown
        print(markdown_output.output_markdown(assessment_results))
    else:
        print(f"Output format {args.output} is not yet implemented.")

    # Placeholder for future functionality
    print(f"Output format: {args.output}")
    print(f"Kubeconfig path: {args.kubeconfig}")
    print(f"Kubernetes context: {args.context}")
    print(f"Assessment level: {args.level}")  # Corrected variable name

if __name__ == "__main__":
    main()
