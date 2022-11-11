from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os
import datetime

fablib = fablib_manager()
print("Initializing network_builder_utils -", "FABLib Configuration")
# fablib.show_config()

# Connection Creation on Slice (with Default Parameter Checking)
# Available L2 Connection Models: 'L2Bridge', 'L2PTP', 'L2STS'
def get_default_network_connection_params():
    default_conn_params = {
        "type": "L2Bridge"
    }
    return default_conn_params

def get_final_network_connection_params(conn_name, conn_params=None, conn_interfaces=None):
    default_params = get_default_network_connection_params()
    if conn_interfaces is None:
        print("network_builder_utils -", "Invalid Set of Interfaces")
        final_params = None
    elif conn_params is None:
        final_params = {param: default_params[param] for param in default_params}
        final_params["name"] = conn_name
        final_params["interfaces"] = conn_interfaces
    else:
        final_params = {"name": conn_name, "interfaces": conn_interfaces}
        for param in default_params:
            if param in conn_params:
                final_params[param] = conn_params[param]
            else:
                final_params[param] = default_params[param]
    return final_params

def add_new_network_connection(slice, conn_name, conn_params=None, conn_interfaces=None):
    final_params = get_final_network_connection_params(conn_name, conn_params, conn_interfaces)
    print("network_builder_utils -", "Final Parameters for New Network Connection:", conn_name, final_params)
    try:
        if final_params["type"].startswith("L2"):
            connection = slice.add_l2network(name=final_params["name"], 
                                             interfaces=final_params["interfaces"])
        else:
            connection = slice.add_l3network(name=final_params["name"], 
                                             interfaces=final_params["interfaces"])
        print("network_builder_utils -", "Created Network Connection Successfully:", conn_name, "in Slice:", slice.get_name())
    except Exception as e:
        print("network_builder_utils -", "Exception in Creating Network Connection:", conn_name, "in Slice:", slice.get_name(), e)
        connection = None
    return connection