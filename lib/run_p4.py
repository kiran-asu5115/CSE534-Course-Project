def get_p4_run_command_for_switch(inst_slice, switch, ethernet_port_mappings, thrift_port=9030):
    command_prefix = "sudo simple_switch "
    thrift_port_command = "--thrift-port " + str(thrift_port) + " "
    interfaces_prefix = "--interface "
    interfaces_command = ""
    program_name = "p4_basic_routing_2"
    program_command = program_name + ".bmv2/" + program_name + ".json"
    for interface in ethernet_port_mappings[switch]:
        interfaces_command += interfaces_prefix + str(ethernet_port_mappings[switch][interface]) + "@" + str(interface) + " "
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