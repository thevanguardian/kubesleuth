def format_console_output(severity, categories, resource_id, message):
	return f'[{severity.upper()}] {categories} - {resource_id}: {message}'

def output_console(results):
	for result in results:
		print(format_console_output(
			result['severity'],
			', '.join(result['categories']),
			result['resource_id'],
			result['message'],
		))
