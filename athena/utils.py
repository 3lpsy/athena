from os.path import abspath, dirname, join

def app_path(path=None):
    if path:
        return join(app_path(), path)
    return abspath(dirname(__file__))

def db_path(path=None):
    if path:
        return join(app_path(), path)
    return abspath(join(app_path(), 'db'))

def root_path(path=None):
    if path:
        return join(root_path(), path)
    return abspath(join(app_path(), '..'))

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
