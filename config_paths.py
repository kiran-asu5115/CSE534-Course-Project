import os

def get_lib_config_path():
    lib_config_path = os.path.join(os.getcwd(), "lib")
    return lib_config_path

def get_project_config_path():
    project_config_path = os.path.join(os.getcwd(), "config", "shik_config", "project_config.json")
    return project_config_path

def get_slice_config_path():
    slice_config_path = os.path.join(os.getcwd(), "config", "slice_config.json")
    return slice_config_path

