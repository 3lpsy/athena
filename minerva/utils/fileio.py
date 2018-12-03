import json
from pathlib import Path
from .paths import minerva_path

def read_minerva_conf():
    _minerva_conf_path = Path(minerva_path("minerva.json"))
    with open(str(_minerva_conf_path), "r", encoding="utf-8") as infile:
        _conf = json.loads(infile.read())
    return _conf

def write_minerva_conf(data):
    _minerva_conf_path = Path(minerva_path("minerva.json"))
    with open(str(_minerva_conf_path), "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, sort_keys=True,indent=4, ensure_ascii=False)

def read_projects_conf():
    _projects_conf_path = Path(minerva_path("projects.json"))
    with open(str(_projects_conf_path), "r", encoding="utf-8") as infile:
        _conf = json.loads(infile.read())
    return _conf

def remove_project_conf(data):
    current_projects = read_projects_conf()
    _projects_conf_path = Path(minerva_path("projects.json"))

    new_conf = []

    for project_conf in current_projects:
        if project_conf["path"] != data['path']:
            new_conf.append(project_conf)

    with open(str(_projects_conf_path), "w", encoding="utf-8") as outfile:
        json.dump(new_conf, outfile, sort_keys=True,indent=4, ensure_ascii=False)

def write_project_conf(data):
    current_projects = read_projects_conf()
    _projects_conf_path = Path(minerva_path("projects.json"))

    new_conf = []

    replace = False
    for project_conf in current_projects:
        if project_conf["path"] == data['path']:
            project_conf = data
            replace = True
        new_conf.append(project_conf)
    if not replace:
        new_conf.append(data)

    with open(str(_projects_conf_path), "w", encoding="utf-8") as outfile:
        json.dump(new_conf, outfile, sort_keys=True,indent=4, ensure_ascii=False)
