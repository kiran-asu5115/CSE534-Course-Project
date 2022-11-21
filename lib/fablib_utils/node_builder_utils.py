from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os

fablib = fablib_manager()
print("Initializing node_builder_utils -", "FABLib Configuration")
# fablib.show_config()
      
      
# Node Creation on Slice (with Default Parameter Checking)
def get_default_node_params():
    default_node_params = {
        "site": "TACC",
        "cores": 2,
        "ram": 8,
        "disk": 50,
        "image": "default_ubuntu_20"
    }
    return default_node_params

def get_final_node_params(node_name, node_params=None):
    default_params = get_default_node_params()
    if node_params is None:
        final_params = {param: default_params[param] for param in default_params}
        final_params["name"] = node_name
    else:
        final_params = {"name": node_name}
        for param in default_params:
            if param in node_params:
                final_params[param] = node_params[param]
            else:
                final_params[param] = default_params[param]
    return final_params

def add_new_node(slice, node_name, node_params=None):
    final_params = get_final_node_params(node_name, node_params)
    print("node_builder_utils -", "Final Parameters for New Node:", final_params)
    try:
        node = slice.add_node(name=final_params["name"], 
                              site=final_params["site"],
                              cores=final_params["cores"], 
                              ram=final_params["ram"], 
                              disk=final_params["disk"], 
                              image=final_params["image"])
        print("node_builder_utils -", "node_builder_utils -", "Created Node Successfully:", node_name)
    except Exception as e:
        print("node_builder_utils -", "Exception in Creating Node:", node_name, e)
        node = None
    return node


