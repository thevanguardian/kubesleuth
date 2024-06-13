from kubesleuth.audit.registry import register_task

@register_task('Security', 'Configuration')
def run():
    print("Running task1.")
