from kubesleuth.audit.registry import register_category

@register_category('General', 'Debugging')
def run():
  categories = run.categories
  return {
    'severity': 'high',
    'categories': categories,
    'resource_id': 'debug/resource1',
    'message': f"Debug message",
  }