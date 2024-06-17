import yaml

def format_yaml_output(threat, categories, resource_id, message):
  return {
    "threat": threat,
    "categories": categories,
    "resource_id": resource_id,
    "message": message
  }

def output_yaml(results):
  formatted_results = [
    format_yaml_output(
        result['threat'],
        result['categories'],
        result['resource_id'],
        result['message']
    )
    for result in results
  ]
  return yaml.dump(formatted_results, sort_keys=False)