"""
Utility functions for converting Python objects to JSON with custom encoding.

The `CustomJSONEncoder` class is a custom JSON encoder that handles datetime objects by converting them to ISO format strings.

The `results_to_json` function takes a Python object and returns a JSON string representation of that object, using the `CustomJSONEncoder` to handle any datetime objects.
"""
import json
from datetime import datetime

# Custom JSON Encoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Utility function to convert results to JSON
def results_to_json(results):
    return json.dumps(results, indent=4, cls=CustomJSONEncoder)
