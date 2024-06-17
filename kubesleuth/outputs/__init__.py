import os
import importlib

output_modules = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith(".py") and f!= "__init__.py"]

for module_name in output_modules:
  importlib.import_module(f'kubesleuth.outputs.{module_name}')