import argparse
from version import __version__

def main():
    parser = argparse.ArgumentParser(description="Kubernetes Configuration Audit by KubeSleuth")
    parser.add_argument("--output", choices=["json", "markdown", "yaml"], default="json", help="Output format (json, markdown, or yaml)")
    parser.add_argument("--kubeconfig", help="Path to the kubeconfig file", default=None)
    parser.add_argument("--context", help="Kubernetes context to use", default=None)
    parser.add_argument("--level", choices=["high", "medium", "low", "info", "debug"], default="all", help="Assessment level to display")
    parser.add_argument("--version", action="version", version=f"{__version__}")
    args = parser.parse_args()

    # Placeholder for future functionality
    print(f"Output format: {args.output}")
    print(f"Kubeconfig path: {args.kubeconfig}")
    print(f"Kubernetes context: {args.context}")
    print(f"Assessment level: {args.level}")

if __name__ == "__main__":
    main()
