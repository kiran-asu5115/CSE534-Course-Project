from lib.fablib_utils import slice_builder_utils
from lib.run_p4 import run_p4_on_topology
from lib.p4_table_configuration import *
from lib.route_configuration import get_final_route, get_complete_p4_route_configurations
import os
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_node_interface_info(inst_slice, avoid_networks=[]):
    node_interface_info = {}
    interfaces = slice_builder_utils.get_slice_interfaces(slice=inst_slice)
    for interface in interfaces:
        node, net = interface.get_node(), interface.get_network().get_name()
        os_int, ip_addr, mac_addr = interface.get_os_interface(), interface.get_ip_addr(), interface.get_mac()
        if net in avoid_networks:
            pass
        elif node in node_interface_info:
            node_interface_info[node][net] = {"os_interface": os_int, "ip_addr": ip_addr, "mac_addr": mac_addr}
        else:
            node_interface_info[node] = {net: {"os_interface": os_int, "ip_addr": ip_addr, "mac_addr": mac_addr}}
    
    for i, src_node in enumerate(node_interface_info):
        for connection in node_interface_info[src_node]:
            for j, dst_node in enumerate(node_interface_info):
                if i == j:
                    pass
                elif connection in node_interface_info[dst_node]:
                    node_interface_info[src_node][connection]['dst_node'] = dst_node
                else:
                    pass
                
    return node_interface_info

slice_name = "Final_Integrated_Topology_3"
inst_slice = slice_builder_utils.get_slice_by_name_or_id(slice_name=slice_name)
avoid_networks = ["_meas_net"]
node_interface_info = get_node_interface_info(inst_slice, avoid_networks)

def get_ethernet_port_mappings(node_interface_info):
    ethernet_port_mappings = {}
    for node in node_interface_info:
        # print("{}:".format(node.get_name()))
        # print(node_interface_info[node])
        mappings = [node_interface_info[node][connection]['os_interface'] for connection in node_interface_info[node]]
        mappings.sort()
        final_mappings = {mappings[i]: i for i in range(len(mappings))}            
        ethernet_port_mappings[node.get_name()] = final_mappings
    print("Ethernet Port Mappings:", ethernet_port_mappings)
    return ethernet_port_mappings

# for node in node_interface_info:
#     print("{}:".format(node.get_name()))
#     print(node_interface_info[node])

ethernet_port_mappings = get_ethernet_port_mappings(node_interface_info)
thrift_port = 9030
run_p4_on_topology(inst_slice, ethernet_port_mappings, thrift_port=thrift_port)

def execute_p4_route_configurations(inst_slice, p4_route_configurations, dst_ip_addr_subnet, ethernet_port_mappings, thrift_port=9030):
    switches = inst_slice.get_nodes()
    for p4_route_config in p4_route_configurations:
        switch_name, _, dst_mac_addr, egress_port, _ = p4_route_config
        switch = [s for s in switches if s.get_name() == switch_name][0]
        params = [dst_mac_addr, str(ethernet_port_mappings[switch_name][egress_port])]
        table_name, action_name = "MyIngress.ipv4_lpm", "MyIngress.ipv4_forward"
        table_dump_entries = execute_p4_table_dump_command(switch, table_name, thrift_port=thrift_port)
        table_ip_entries = parse_dump_entries(table_dump_entries)
        if dst_ip_addr_subnet in table_ip_entries:
            handle_id = str(table_ip_entries[dst_ip_addr_subnet])
            execute_p4_modify_entry_command(switch, table_name, action_name, handle_id, params, thrift_port)
        else:
            execute_p4_add_entry_command(switch, table_name, action_name, dst_ip_addr_subnet, params, thrift_port)
        
def add_complete_route(inst_slice, all_routes, node_interface_info, ethernet_port_mappings, src_host, dst_host, thrift_port, pick_route=None):
    route = get_final_route(all_routes, src_host, dst_host, pick_route)
    p4_route_configurations = get_complete_p4_route_configurations(node_interface_info, route)
    dst_ip_addr = p4_route_configurations[-1][-1]
    dst_ip_addr_subnet = ".".join(dst_ip_addr.split(".")[0:3]) + ".0/24"
    print("Destination IP Address: {} Destination IP Address Subnet {}".format(dst_ip_addr, dst_ip_addr_subnet))
    execute_p4_route_configurations(inst_slice, p4_route_configurations, dst_ip_addr_subnet, ethernet_port_mappings, thrift_port)
    
host_routes = {}
host_routes["Host_1"] = {
    "Host_2": [["Host_1", "Switch_1", "Switch_2", "Host_2"], ["Host_1", "Switch_1", "Switch_3", "Switch_4", "Switch_2", "Host_2"]],
    "Host_3": [["Host_1", "Switch_1", "Switch_3", "Host_3"], ["Host_1", "Switch_1", "Switch_2", "Switch_4", "Switch_3", "Host_3"]],
    "Host_4": [["Host_1", "Switch_1", "Switch_2", "Switch_4", "Host_4"], ["Host_1", "Switch_1", "Switch_3", "Switch_4", "Host_4"]]
}
host_routes["Host_2"] = {
    "Host_1": [["Host_2", "Switch_2", "Switch_1", "Host_1"], ["Host_2", "Switch_2", "Switch_4", "Switch_3", "Switch_1", "Host_1"]],
    "Host_4": [["Host_2", "Switch_2", "Switch_4", "Host_4"]]
}
host_routes["Host_3"] = {
    "Host_1": [["Host_3", "Switch_3", "Switch_1", "Host_1"], ["Host_3", "Switch_3", "Switch_4", "Switch_2", "Switch_1", "Host_1"]],
    "Host_4": [["Host_3", "Switch_3", "Switch_4", "Host_4"]]
}
host_routes["Host_4"] = {
    "Host_1": [["Host_4", "Switch_4", "Switch_2", "Switch_1", "Host_1"], ["Host_4", "Switch_4", "Switch_3", "Switch_1", "Host_1"]],
    "Host_2": [["Host_4", "Switch_4", "Switch_2", "Host_2"], ["Host_4", "Switch_4", "Switch_3", "Switch_1", "Switch_2", "Host_2"]],
    "Host_3": [["Host_4", "Switch_4", "Switch_3", "Host_3"], ["Host_4", "Switch_4", "Switch_2", "Switch_1", "Switch_3", "Host_3"]]
}

@app.route("/update_route", methods=["POST"])
def update_route():
    # src_host, dst_host = "Host_3", "Host_4"
    # add_complete_route(inst_slice, host_routes, node_interface_info, ethernet_port_mappings, src_host, dst_host, thrift_port, pick_route=1)
    pass


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret_101$'
    app.run(host="0.0.0.0", port=5082, debug=True)
