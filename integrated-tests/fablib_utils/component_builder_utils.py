from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os

fablib = fablib_manager()
print("Initializing component_builder_utils -", "FABLib Configuration")
# fablib.show_config()
      
# Component Creation on Node (with Default Parameter Checking)
# Available Component Models: 'NIC_Basic', 'NIC_ConnectX_6', 'NIC_ConnectX_5', 'NVME_P4510', 'GPU_TeslaT4', 'GPU_RTX6000'
def get_default_component_params():
    default_comp_params = {
        "model": "NIC_Basic"
    }
    return default_comp_params

def get_final_component_params(comp_name, comp_params=None):
    default_params = get_default_component_params()
    if comp_params is None:
        final_params = {param: default_params[param] for param in default_params}
        final_params["name"] = comp_name
    else:
        final_params = {"name": comp_name}
        for param in default_params:
            if param in comp_params:
                final_params[param] = comp_params[param]
            else:
                final_params[param] = default_params[param]
    return final_params

def add_new_component(node, comp_name, comp_params=None):
    final_params = get_final_component_params(comp_name, comp_params)
    print("component_builder_utils -", "Final Parameters for New Component:", final_params)
    try:
        component = node.add_component(name=final_params["name"], 
                                       model=final_params["model"])
        print("component_builder_utils -", "Created Component Successfully:", comp_name, "for Node:", node.get_name())
    except Exception as e:
        print("component_builder_utils -", "Exception in Creating Component:", comp_name, "in Node:", node.get_name(), e)
        component = None
    return component

def get_interface_of_component(component, interface_number):
    interfaces = component.get_interfaces()
    print("component_builder_utils -", "No. of Interfaces:", len(interfaces))
    print("component_builder_utils -", "Component Interfaces", interfaces)
    if interface_number <= 0 or interface_number > len(interfaces):
        print("component_builder_utils -", "Invalid Interface Number entered")
        interface = None
    else:
        interface = interfaces[interface_number - 1]
    return interface

