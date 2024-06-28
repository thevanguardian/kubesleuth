# Contributing New Tasks to KubeSleuth

Welcome to the `tasks` directory of KubeSleuth! This document provides guidelines and instructions for contributing new tasks to the KubeSleuth project. Please follow these guidelines to ensure consistency and quality in our codebase.

## Guidelines for Adding New Tasks

1. **Filename and Classname**:
   - The filename and the classname must match. For example, if the filename is `NodeHealth.py`, the class inside it should be named `NodeHealth`.

2. **Categories**:
   - Each task must be registered with appropriate categories using the `@register_category` decorator. This allows tasks to be dynamically discovered and executed based on their categories.

3. **Implementation Plan**:
   - At the top of each task file, include a comment with an implementation plan. This should outline the steps and logic of the task.

4. **Threat Levels**:
   - Use the following threat levels for reporting issues:
     - `Critical`
     - `Warn`
     - `Info`
     - `Debug` (for detailed information)

5. **Output Formatting**:
   - Ensure the task results include nested sub-messages for detailed checks.
   - Set `resource_id` to the filename without the extension.

6. **Error Handling and Logging**:
   - Include robust error handling and logging for auditing purposes.

## Example Task

Here is an example of a properly structured task file:

```python
# MyNewTask.py

# Implementation Plan
# - Describe the steps and logic of the task here.

import os
import logging
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubesleuth.audit.registry import register_category

logger = logging.getLogger(__name__)

@register_category('Category1', 'Category2')  # Specify appropriate categories
class MyNewTask:
    
    def __init__(self):
        self.categories = self.__class__.categories  # Initialize categories from class attribute
        config.load_kube_config()
        self.v1_core = client.CoreV1Api()
        self.resource_id = os.path.splitext(os.path.basename(__file__))[0]  # Set resource_id to filename sans extension

    def run(self) -> dict:
        # Implement the task logic here.
        results = {
            'threat': 'info',
            'categories': self.categories,
            'resource_id': self.resource_id,
            'message': 'My new task compliance scan.',
            'sub_messages': []
        }

        # Example sub-message
        results['sub_messages'].append({
            'threat': 'warn',
            'resource_id': 'example_resource',
            'message': 'This is an example warning message.'
        })

        return results
