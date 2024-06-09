# KubeSleuth

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.18%2B-blue)
![License](https://img.shields.io/badge/license-GPL%20v3-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

![KubeSleuth](kube-sleuth.png)


KubeSleuth is a simple tool for auditing your Kubernetes clusters. It scans your cluster configurations for misconfigurations, best practices, security issues, and resource allocations, providing detailed reports to help you maintain a healthy and secure environment.

It's still in early development, so expect some rough edges.

## Table of Contents

- [How to Use](#how-to-use)
- [Overview](#overview)
- [Installation](#installation)
- [Features](#features)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## How to Use

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/kubesleuth.git
    cd kubesleuth
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run KubeSleuth**:
    ```bash
    python3 kubesleuth.py --output markdown
    ```

4. **Optional arguments**:
    - `--kubeconfig`: Path to the kubeconfig file (default: `$HOME/.kube/config`)
    - `--context`: Kubernetes context to use

    Example:
    ```bash
    python3 kubesleuth.py --output json --kubeconfig /path/to/kubeconfig --context my-context
    ```

## Overview

KubeSleuth is designed to help you maintain a secure and well-configured Kubernetes cluster. It performs a variety of checks on your cluster, including:

- **RBAC (Role-Based Access Control)**: Ensures role bindings are secure and correctly configured.
- **Authentication**: Checks for basic authentication and password policies.
- **Custom Roles**: Identifies and reviews custom roles and cluster roles.
- **Network Policies**: Ensures network policies are defined and enforced.
- **Namespace Isolation**: Checks if resources are properly isolated by namespaces.
- **Privileged Containers**: Detects containers running with privileged access.

By running KubeSleuth, you can quickly identify potential issues and areas for improvement in your cluster's configuration.

## Installation

To install KubeSleuth, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/thevanguardian/kubesleuth.git
    cd kubesleuth
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Features

- **RBAC Audit**: Identifies insecure role bindings and missing subjects.
- **Authentication Checks**: Verifies if basic authentication is enabled.
- **Custom Roles Review**: Lists and reviews custom roles and cluster roles.
- **Network Policies Audit**: Ensures network policies are present and enforced.
- **Namespace Isolation Checks**: Detects resources placed in the default namespace.
- **Privileged Containers Detection**: Finds containers running with privileged access.
- **Flexible Configuration**: Supports custom kubeconfig files and contexts.

## Configuration

KubeSleuth can be configured using command-line arguments:

- `--kubeconfig`: Path to the kubeconfig file (default: `$HOME/.kube/config`)
- `--context`: Kubernetes context to use
- `--output`: Output format (`json` or `markdown`)

Example:
```bash
python3 kubesleuth.py --output markdown --kubeconfig /path/to/kubeconfig --context my-context
```
## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please create an issue or submit a pull request.

Fork the repository
Create your feature branch (git checkout -b feature/your-feature)
Commit your changes (git commit -m 'Add your feature')
Push to the branch (git push origin feature/your-feature)
Open a pull request

## License
This project is licensed under the GNU General Public License v3 (GPLv3).