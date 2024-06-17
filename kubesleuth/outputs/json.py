import json

def format_json_output(threat, categories, resource_id, message):
  return {
    "threat": threat,
    "categories": categories,
    "resource_id": resource_id,
    "message": message
  }

def output_json(results):
  formatted_results = [
    format_json_output(
        result['threat'],
        result['categories'],
        result['resource_id'],
        result['message']
    )
    for result in results
  ]
  return json.dumps(formatted_results, indent=2)