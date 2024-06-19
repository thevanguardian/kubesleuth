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
        """
        Format the output based on the specified format and optionally write to a file.
        :param results: List of results to format.
        """
        results = self.convert_tuples_to_lists(results)  # Convert tuples to lists

        try:
            if self.output_format == 'markdown':
                template = self.env.get_template('audit_template.md.j2')
                output = template.render(results=results)
            elif self.output_format == 'yaml':
                output = yaml.dump(results, sort_keys=False)
            elif self.output_format == 'json':
                output = json.dumps(results, indent=2)
            else:  # Console output
                output = self.format_console_output(results)
        except TemplateNotFound as e:
            logger.error(f"Template not found: {e}")
            return
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return

        if self.output_file:
            try:
                with open(self.output_file, 'w') as f:
                    f.write(output)
            except Exception as e:
                logger.error(f"Error writing to output file: {e}")
        else:
            print(output)

    def format_console_output(self, results):
        """
        Format the console output with nested sub-messages.
        :param results: List of results to format.
        :return: Formatted console output as a string.
        """
        output = ''
        for result in results:
            output += f"Threat Level: {result['threat'].upper()}\n"
            output += f"Resource ID: {result['resource_id']}\n"
            output += f"Categories: {', '.join(result['categories'])}\n"
            output += f"Message: {result['message']}\n"
            if 'sub_messages' in result:
                for sub_message in result['sub_messages']:
                    output += f"  - Threat Level: {sub_message['threat'].upper()}\n"
                    output += f"    Resource ID: {sub_message['resource_id']}\n"
                    output += f"    Message: {sub_message['message']}\n"
        return output

    def convert_tuples_to_lists(self, results):
        """
        Convert all tuples in the results to lists.
        :param results: List of results.
        :return: Results with tuples converted to lists.
        """
        if isinstance(results, list):
            return [self.convert_tuples_to_lists(item) for item in results]
        elif isinstance(results, dict):
            return {key: self.convert_tuples_to_lists(value) for key, value in results.items()}
        elif isinstance(results, tuple):
            return list(results)
        else:
            return results
