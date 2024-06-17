import json
def format_json_output(results):
  return json.dumps(results, indent=4)

def output_json(results):
  try:
    print(format_json_output(results))
  except (TypeError, ValueError) as e:
    print(f"Error in JSON output: {e}.")