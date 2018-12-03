from os.path import abspath, dirname, join
from pathlib import Path
from minerva.logger import logger
from shutil import copy, copytree
from .fileio import write_minerva_conf
from .paths import minerva_path, data_path

def ensure_minerva_is_ready():
    _minerva_path = Path(minerva_path())
    if not _minerva_path.is_dir():
        logger().info("Making minerva directory at {}".format(_minerva_path))
        Path(minerva_path()).mkdir()
    _minerva_conf_path = Path(minerva_path("minerva.json"))
    if not _minerva_conf_path.is_file():
        logger().info("Making minerva conf file at {}".format(str(_minerva_conf_path)))
        minerva_conf_data = {}
        minerva_conf_data["conf_dir"] = minerva_path()
        minerva_conf_data["log_path"] = minerva_path("minerva.log")
        minerva_conf_data["log_level"] = "INFO"
        minerva_conf_data["loaded"] = 0
        write_minerva_conf(minerva_conf_data)
            # can set other binary paths later

    _minerva_projects_path = Path(minerva_path("projects.json"))
    if not _minerva_projects_path.is_file():
        logger().info("Copying minerva projects template to {}".format(str(_minerva_projects_path)))
        copy(data_path('projects.json.template'), str(_minerva_projects_path))
        copy(data_path('projects.json.example'), str(minerva_path("projects.json.example")))
    _minerva_load_data_path = Path(minerva_path("load"))
    if not _minerva_load_data_path.is_dir():
        logger().info("Copying loadable minerva data to {}".format(str(_minerva_load_data_path)))
        copytree(data_path('load'), str(_minerva_load_data_path))
