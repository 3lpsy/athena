from os.path import abspath, dirname, join
from pathlib import Path

def minerva_path(path=None):
    user_home = str(Path.home())
    _minerva_path = join(user_home, ".minerva")
    if path:
        return abspath(join(_minerva_path, path))
    return abspath(_minerva_path)

def app_path(path=None):
    if path:
        return join(abspath(join(dirname(__file__)), '..'), path)
    return abspath(join(dirname(__file__), '..'))

def db_path(path=None):
    _db_path = join(app_path(), 'db')
    if path:
        return join(_db_path, path)
    return abspath(_db_path)

def data_path(path=None):
    _data_path = join(app_path(), 'data')
    if path:
        return join(_data_path, path)
    return abspath(_data_path)

def root_path(path=None):
    _root_path = join(app_path(), '..')
    if path:
        return join(_root_path, path)
    return abspath(_root_path)
