task_registry = {}

def register_category(*categories):
	def decorator(func):
		func.categories = categories  # Store categories in the function
		for category in categories:
			if category not in task_registry:
				task_registry[category] = []
			task_registry[category].append(func)
		return func
	return decorator

def get_tasks_by_category(category):
	return task_registry.get(category, [])

def get_available_categories():
	return list(task_registry.keys())
