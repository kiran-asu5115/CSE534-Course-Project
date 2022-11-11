import json
import os

import sys
print(os.path.join(os.getcwd(), "lib"))
sys.path.insert(0, os.path.join(os.getcwd(), "lib"))
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


set_environ("project_config.json")
slice_config = read_config("config/slice_config.json")
# s = SetupSlice(slice_config)
# s.get_slice_ssh_commands()
# s.configure_ips()
# int = Instrumentize(slice_config["slice_name"])
