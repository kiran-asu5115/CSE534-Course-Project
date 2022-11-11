import json
import os

from lib.setup_elk_grafana import Instrumentize
from lib.slice_builder import SetupSlice


def set_environ(filename):
    with open(filename, "r+") as fp:
        data = json.load(fp)
    for key, value in data.items():
        os.environ[key] = value


def read_config(filename):
    with open(filename, "r+") as fp:
        data = json.load(fp)
    return data


set_environ("config/shik_config/project_config.json")
slice_config = read_config("config/slice_config.json")
s = SetupSlice(slice_config)
int = Instrumentize(slice_config["slice_name"])
int.upload_grafana_dashboard()
