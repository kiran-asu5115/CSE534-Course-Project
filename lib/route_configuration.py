import random
import os

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
        print("Cannot find Connection between Source {} / Destiantion Host {} in Node Interface Info".format(src_host, dst_host))
        return None
    else:
        final_connection = src_dst_conn
    
    src_egress_port = src_host_info[final_connection]['os_interface']
    dst_port_mac_addr = dst_host_info[final_connection]['mac_addr']
    dst_host_ip_addr = dst_host_info[final_connection]['ip_addr']
    return final_connection, dst_port_mac_addr, src_egress_port, dst_host_ip_addr

def get_final_route(all_routes, src_host, dst_host, pick_route=None):
    if src_host not in all_routes:
        print("No Routes available for Source Host:", src_host, "in Routes:", all_routes)
        return None
    if dst_host not in all_routes[src_host]:
        print("No Routes available to Destination Host:", dst_host, "from Source Host:", src_host, "in Routes:", all_routes)
        return None
    
    available_routes = all_routes[src_host][dst_host]
    n = len(available_routes)
    if n == 0: 
        print("Zero Routes available to Destination Host:", dst_host, "from Source Host:", src_host, "in Routes:", all_routes)
        return None
    if n == 1:
        final_route = available_routes[0]
    elif pick_route is None:  # Pick an Arbitrary Route if Multiple Routes found & no Preferences given
        route_no = random.randint(0, n - 1)
        final_route = available_routes[route_no]
    elif 0 < pick_route <= n:
        final_route = available_routes[pick_route - 1]
    else:
        print("Invalid Route Picked!")
        return None
        
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