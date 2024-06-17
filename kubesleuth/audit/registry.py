from collections import defaultdict

task_registry = defaultdict(set) # Assign this as a set, so there are no duplicate task names
threat_registry = defaultdict(set) # Assign this as a set, so there are no duplicate threat names

def register_category(*categories):
	def decorator(func):
		func.categories = categories  # Store categories in the function
		for category in categories:
			task_registry[category].add(func) # Add category to task_registry set
		return func
	return decorator

def register_threat(*threats):
	def decorator(func):
		func.threats = threats  # Store threats in the function
		for threat in threats:
			threat_registry[threat].add(func) # Add threat to threat_registry set
		return func
	return decorator

def get_tasks_by_category(category):
	return task_registry.get(category, set())

def get_tasks_by_threat(threat):
	return threat_registry.get(threat, set())

def get_available_categories():
	return list(task_registry.keys())

def get_available_threats():
	return list(threat_registry.keys())
