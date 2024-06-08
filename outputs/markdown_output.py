"""
Generates a Markdown report from the provided results using a Jinja2 template.

Args:
    results (dict): A dictionary containing the results to be rendered in the Markdown report.

Returns:
    str: The generated Markdown report.
"""
from jinja2 import Environment, FileSystemLoader
import os

def results_to_markdown(results):
    # Load the Jinja2 template
    template_loader = FileSystemLoader(searchpath=os.path.join(os.path.dirname(__file__), '..', 'templates'))
    template_env = Environment(loader=template_loader)
    template = template_env.get_template('audit_template.md.j2')

    # Render the template with the results
    markdown_output = template.render(results=results)
    return markdown_output
