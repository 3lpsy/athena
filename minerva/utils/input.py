
def confirm(message, options=None, truthy=None):
    options = options or ['Y', 'n']
    truthy = ['Y']
    suffix = " [" + ''.join([o + '/' for o in options]).strip('/') + ']: '
    answer = input(message + suffix).strip()
    while True:
        if answer not in options:
            print('Incorrect option. Try again.')
            answer = input(message + suffix).strip()
            continue
        if answer in truthy:
            return True
        return False
