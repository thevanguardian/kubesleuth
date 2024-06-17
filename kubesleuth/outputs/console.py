def format_console_output(threat, categories, resource_id, message):
	return f'[{threat.upper()}] {categories} - {resource_id}: {message}'

def output_console(results):
	for result in results:
		try:
			print(format_console_output(
				result['threat'],
				', '.join(result['categories']),
				result['resource_id'],
				result['message'],
			))
		except KeyError as e:
			print(f"Error in result formatting: Missing key {e}.")
