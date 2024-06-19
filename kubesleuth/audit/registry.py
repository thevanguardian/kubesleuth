from collections import defaultdict

task_registry = defaultdict(set) # Assign this as a set, so there are no duplicate task names

def register_category(*categories):
	def decorator(func):
		func.categories = categories  # Store categories in the function
		for category in categories:
			task_registry[category].add(func) # Add category to task_registry set
		return func
	return decorator

def get_tasks_by_category(category):
	return task_registry.get(category, set())

def get_available_categories():
	return list(task_registry.keys())

