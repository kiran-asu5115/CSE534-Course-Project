import os
import sys
import json

sys.path.insert(0, os.path.join(os.getcwd(), "lib"))


def set_environ(filename):
    with open(filename, "r+") as fp:
        data = json.load(fp)
    for key, value in data.items():
        os.environ[key] = value


set_environ("project_config.json")

from lib.slice_builder import SetupSlice
from lib.setup_elk_grafana import Instrumentize


def read_config(filename):
    with open(filename, "r+") as fp:
        data = json.load(fp)
    return data


slice_config = read_config("config/slice_config.json")
s = SetupSlice(slice_config)
# s.create_slice()
s.get_slice_ssh_commands()
s.configure_ips()
# int = Instrumentize(slice_config["slice_name"])
