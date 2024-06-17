from kubesleuth.audit.registry import register_category, register_threat

@register_category('General', 'Debugging')
@register_threat('high')
def run():
  categories = run.categories
  threat = run.threats[0]
  return {
    'threat': threat,
    'categories': categories,
    'resource_id': 'debug/resource-1',
    'message': f"Debug message",
  }