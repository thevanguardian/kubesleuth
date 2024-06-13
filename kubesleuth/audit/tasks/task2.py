from kubesleuth.audit.registry import register_task

@register_task('Security', 'User')
def run():
    print("Running task2.")