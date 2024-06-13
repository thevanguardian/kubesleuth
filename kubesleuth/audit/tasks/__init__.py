import os
import importlib

# Dynamically import all task modules
task_modules = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith(".py") and f != "__init__.py"]

print(f"Loading tasks: {task_modules}")

for module_name in task_modules:
  importlib.import_module(f'kubesleuth.audit.tasks.{module_name}')