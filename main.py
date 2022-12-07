import os
import sys
import json

from config_paths import get_lib_config_path, get_project_config_path, get_slice_config_path

lib_config_path = get_lib_config_path()
sys.path.insert(0, lib_config_path)


def set_environ(filename):
    with open(filename, "r+") as fp:
        data = json.load(fp)
    for key, value in data.items():
        os.environ[key] = value


project_config_path = get_project_config_path()
set_environ(project_config_path)


from lib.slice_builder import MeasurementSlice
from lib.setup_elk_grafana import Instrumentize


def read_config(filename):
    with open(filename, "r+") as fp:
        data = json.load(fp)
    return data


def main():
    slice_config_file_name = "config_test.json"
    slice_config_path = get_slice_config_path(file_name=slice_config_file_name)
    slice_config = read_config(slice_config_path)
    s = MeasurementSlice(slice_config)
    s.create_slice()
    s.get_slice_ssh_commands()
    s.configure_ips()
    s.add_config_files_to_slice_nodes()

    # inst_slice = Instrumentize(slice_config["slice_name"])


if __name__ == '__main__':
    main()
