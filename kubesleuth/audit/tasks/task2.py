from kubesleuth.audit.registry import register_category, register_threat

@register_category('Configuration', 'User', 'General')
@register_threat('medium')
def run():
  categories = run.categories
  threat = run.threats[0]
  return {
    'threat': threat,
    'categories': categories,
    'resource_id': 'resource2',
    'message': f"Task2 check"
  }
