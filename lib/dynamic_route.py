from lib.fablib_utils import slice_builder_utils
import os
import random
from flask import Flask, jsonify, request





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


# slice_name = "Final_Integrated_Topology_3"
# inst_slice = slice_builder_utils.get_slice_by_name_or_id(slice_name=slice_name)
# avoid_networks = ["_meas_net"]
# node_interface_info = get_node_interface_info(inst_slice, avoid_networks)


def get_ethernet_port_mappings(node_interface_info):
    ethernet_port_mappings = {}
    for node in node_interface_info:
        # print("{}:".format(node.get_name()))
        # print(node_interface_info[node])
        mappings = {}
        for i, connection in enumerate(node_interface_info[node]):
            mappings[node_interface_info[node][connection]['os_interface']] = i
        ethernet_port_mappings[node.get_name()] = mappings
    print("Ethernet Port Mappings:", ethernet_port_mappings)
    return ethernet_port_mappings


def get_p4_run_command_for_switch(inst_slice, switch, ethernet_port_mappings, thrift_port=9030):
    command_prefix = "sudo simple_switch "
    thrift_port_command = "--thrift-port " + str(thrift_port) + " "
    interfaces_prefix = "--interface "
    interfaces_command = ""
    program_name = "p4_basic_routing_2"
    program_command = program_name + ".bmv2/" + program_name + ".json"
    for interface in ethernet_port_mappings[switch]:
        interfaces_command += interfaces_prefix + ethernet_port_mappings[switch][interface] + "@" + str(interface) + " "
    final_command = command_prefix + thrift_port_command + interfaces_command + program_command
    print(switch, final_command)
    return final_command


def start_p4_on_switch(switch_commands):
    switch_nodes = [x for x in inst_slice.get_nodes() if x.get_name().startswith("Switch")]
    for switch in switch_nodes:
        print("Switching on P4 for Switch:", switch.get_name())
        switch.execute_thread(switch_commands[switch.get_name()])


def run_p4_on_topology(inst_slice, ethernet_port_mappings, thrift_port=9030):
    switch_nodes = [x.get_name() for x in inst_slice.get_nodes() if x.get_name().startswith("Switch")]
    print("Switch Nodes", switch_nodes)
    final_commands = {}
    for switch in switch_nodes:
        final_commands[switch] = get_p4_run_command_for_switch(inst_slice, switch, ethernet_port_mappings, thrift_port)
    start_p4_on_switch(final_commands)


# ethernet_port_mappings = get_ethernet_port_mappings(node_interface_info)
# thrift_port = 9030
# run_p4_on_topology(inst_slice, ethernet_port_mappings, thrift_port=thrift_port)


def get_host_info(info, host):
    host_info = None
    for h in info:
        if h.get_name() == host:
            host_info = node_interface_info[h]
            break
    return host_info


def get_connection_info(info, endpoint):
    for connection in info:
        if info[connection]["dst_node"].get_name() == endpoint:
            return connection
        else:
            pass
    return None


def get_configuration_info(node_interface_info, src_host, dst_host):
    src_host_info = get_host_info(node_interface_info, src_host)
    dst_host_info = get_host_info(node_interface_info, dst_host)
    if src_host_info is None or dst_host_info is None:
        print("Cannot find Source Host {} / Destination Host {} in Node Interface Info".format(src_host, dst_host))
        return None
    else:
        pass

    src_dst_conn = get_connection_info(src_host_info, endpoint=dst_host)
    dst_src_conn = get_connection_info(dst_host_info, endpoint=src_host)
    if src_dst_conn is None or dst_src_conn is None or src_dst_conn != dst_src_conn:
        print("Cannot find Connection between Source {} / Destiantion Host {} in Node Interface Info".format(src_host,
                                                                                                             dst_host))
        return None
    else:
        final_connection = src_dst_conn

    src_egress_port = src_host_info[final_connection]['os_interface']
    dst_port_mac_addr = dst_host_info[final_connection]['mac_addr']
    dst_host_ip_addr = dst_host_info[final_connection]['ip_addr']
    return final_connection, dst_port_mac_addr, src_egress_port, dst_host_ip_addr


def get_final_route(all_routes, src_host, dst_host):
    if src_host not in all_routes:
        print("No Routes available for Source Host:", src_host, "in Routes:", all_routes)
        return
    if dst_host not in all_routes[src_host]:
        print("No Routes available to Destination Host:", dst_host, "from Source Host:", src_host, "in Routes:",
              all_routes)
        return

    available_routes = all_routes[src_host][dst_host]
    n = len(available_routes)
    if n == 0:
        print("Zero Routes available to Destination Host:", dst_host, "from Source Host:", src_host, "in Routes:",
              all_routes)
        return
    if n == 1:
        final_route = available_routes[0]
    else:
        route_no = random.randint(0, n - 1)
        final_route = available_routes[route_no]
    print("Using Route:", final_route)
    return final_route


def get_complete_p4_route_configurations(node_configuration_info, route):
    route_configurations = []
    for i in range(0, len(route) - 1, 1):
        src, dst = route[i], route[i + 1]
        if src.startswith("Host"):
            pass
        else:
            configuration = get_configuration_info(node_interface_info, src, dst)
            if configuration is None:
                print("Aborting Configutation")
                return None
            else:
                route_configurations.append([src] + list(configuration))
    print("Route Configurations for Route:", route, "->", route_configurations)
    return route_configurations


def upload_p4_command_file(inst_slice, switch, p4_commands):
    p4_command_file_name = switch.get_name() + "_Command.txt"
    p4_command_file_path = os.path.join(os.getcwd(), "lib", "p4_commands", p4_command_file_name)
    with open(p4_command_file_path, "w") as f:
        f.writelines(p4_commands)
    switch.upload_file(p4_command_file_path, p4_command_file_name)
    return p4_command_file_name


def execute_p4_route_configurations(inst_slice, p4_route_configurations, dst_ip_addr_subnet, ethernet_port_mappings,
                                    thrift_port=9030):
    switches = inst_slice.get_nodes()
    p4_command_prefix = "table_add MyIngress.ipv4_lpm MyIngress.ipv4_forward "
    p4_run_command = "simple_switch_CLI --thrift-port " + str(thrift_port)
    ip_addr_command = dst_ip_addr_subnet + " => "
    for p4_route_config in p4_route_configurations:
        switch_name, _, dst_mac_addr, egress_port, _ = p4_route_config
        switch = [s for s in switches if s.get_name() == switch_name][0]
        mac_port_command = dst_mac_addr + " " + str(ethernet_port_mappings[switch_name][egress_port])
        full_p4_config_command = p4_command_prefix + ip_addr_command + mac_port_command
        print(switch_name, full_p4_config_command)
        file_name = upload_p4_command_file(inst_slice, switch, [full_p4_config_command])
        full_p4_exec_command = p4_run_command + " < " + file_name
        print("Executing P4 Add Table Command for Switch:", switch_name, ":", full_p4_exec_command)
        switch.execute_thread(full_p4_exec_command)


def add_complete_route(inst_slice, all_routes, node_interface_info, ethernet_port_mappings, src_host, dst_host,
                       thrift_port):
    route = get_final_route(all_routes, src_host, dst_host)
    p4_route_configurations = get_complete_p4_route_configurations(node_interface_info, route)
    dst_ip_addr = p4_route_configurations[-1][-1]
    dst_ip_addr_subnet = ".".join(dst_ip_addr.split(".")[0:3]) + ".0/24"
    print("Destination IP Address: {} Destination IP Address Subnet {}".format(dst_ip_addr, dst_ip_addr_subnet))
    execute_p4_route_configurations(inst_slice, p4_route_configurations, dst_ip_addr_subnet, ethernet_port_mappings,
                                    thrift_port)


host_routes = {}
host_routes["Host_1"] = {
    "Host_2": [["Host_1", "Switch_1", "Switch_2", "Host_2"],
               ["Host_1", "Switch_1", "Switch_3", "Switch_4", "Switch_2", "Host_2"]]
}
host_routes["Host_2"] = {
    "Host_1": [["Host_2", "Switch_2", "Switch_1", "Host_1"],
               ["Host_2", "Switch_2", "Switch_4", "Switch_3", "Switch_1", "Host_1"]]
}
src_host, dst_host = "Host_1", "Host_2"
add_complete_route(inst_slice, host_routes, node_interface_info, ethernet_port_mappings, src_host, dst_host,
                   thrift_port)
src_host, dst_host = "Host_2", "Host_1"
add_complete_route(inst_slice, host_routes, node_interface_info, ethernet_port_mappings, src_host, dst_host, thrift_port)

app = Flask(__name__)


@app.route("/update_route", methods=["POST"])
def update_route():
    pass


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret_101$'
    app.run(host="0.0.0.0", port=5082, debug=True)
