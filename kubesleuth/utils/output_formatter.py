import os
import json
import yaml
import logging
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

logger = logging.getLogger(__name__)

class OutputFormatter:
  def __init__(self, output_format, output_file=None):
    self.output_format = output_format
    self.output_file = output_file
    self.env = Environment(loader=FileSystemLoader('templates'))

  def format_output(self, results):
    try:
      if self.output_format == 'markdown':
        template = self.env.get_template('audit_template.md.j2')
        output = template.render(results=results)
      elif self.output_format == 'yaml':
        output = yaml.dump(results, sort_keys=False)
      elif self.output_format == 'json':
        output = json.dumps(results)
      else:  # Console output
        output = '\n'.join([f"Threat Level: {result['threat'].upper()}\n"
                            f"Resource ID: {result['resource_id']}\n"
                            f"Categories: {', '.join(result['categories'])}\n"
                            f"Message: {result['message']}\n"
                            for result in results])
    except TemplateNotFound as e:
      logger.error(f"Template not found: {e}")
      return
    except Exception as e:
      logger.error(f"Unexpected error occured: {e}")

    if self.output_file:
      try:
        with open(self.output_file, 'w') as f:
          f.write(output)
      except Exception as e:
        logger.error(f"Error writing to output file: {e}")
    else:
      print(output)
