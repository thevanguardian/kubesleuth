from jinja2 import Environment, FileSystemLoader

def format_markdown_output(threat, categories, resource_id, message):
  return {
    "threat": threat,
    "categories": categories,
    "resource_id": resource_id,
    "message": message
  }

def output_markdown(results):
  env = Environment(loader=FileSystemLoader('kubesleuth/templates'))
  template = env.get_template('audit_template.md.j2')

  formatted_results = [
    format_markdown_output(
      threat=result['threat'],
      categories=result['categories'],
      resource_id=result['resource_id'],
      message=result['message']
    )
    for result in results
  ]

  return template.render(results=formatted_results)