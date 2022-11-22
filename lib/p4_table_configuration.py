def get_ip_from_hex(hex_ip):
    if len(hex_ip) == 8:
        addr = []
        for i in range(0, len(hex_ip), 2):
            addr.append(str(int(hex_ip[i:i+2], base=16)))
        return ".".join(addr)
    else:
        print("Invalid IPv4 Address!!")
        return None
    
def parse_dump_entries(lines):
    ip_entries = {}
    curr_entry_handle = ""
    parse_next = False
    for line in lines:
        if parse_next is True:
            ip_addr_complete = line.split()[-1]
            ip_addr, ip_addr_subnet = ip_addr_complete.split("/")
            int_ip = ip_addr if "." in ip_addr else get_ip_from_hex(ip_addr)
            final_ip = int_ip + "/" + ip_addr_subnet
            ip_entries[final_ip] = curr_entry_handle 
            parse_next = False
        elif line.startswith("Dumping entry"):
            curr_entry_handle = line.split()[-1]
            curr_entry_handle = int(curr_entry_handle, base=16) if "x" in curr_entry_handle else int(curr_entry_handle)
        elif line.startswith("Match key"):
            parse_next = True
        else:
            pass
    print("IP Entries:", ip_entries)
    return ip_entries

def execute_p4_table_dump_command(switch, table_name, thrift_port=9030):
    p4_command_prefix = "echo \"table_dump"
    p4_command_args = [p4_command_prefix, table_name, "\""]
    p4_run_command = "simple_switch_CLI --thrift-port " + str(thrift_port)
    p4_dump_command = " ".join(p4_command_args) + " | " + p4_run_command
    print("Executing P4 Table Dump Command:", p4_dump_command, "on Switch:", switch.get_name())
    stdout = switch.execute(p4_dump_command)
    return stdout[0].split("\n")

def execute_p4_add_entry_command(switch, table_name, action_name, addr, params, thrift_port=9030):
    p4_command_prefix = "echo \"table_add"
    p4_command_args = [p4_command_prefix, table_name, action_name, addr, "=>"] + params + ["\""]
    p4_run_command = "simple_switch_CLI --thrift-port " + str(thrift_port)
    p4_add_command = " ".join(p4_command_args) + " | " + p4_run_command
    print("Executing P4 Add Command:", p4_add_command, "on Switch:", switch.get_name())
    stdout = switch.execute(p4_add_command)
    print("Add Command Result:", stdout)

def execute_p4_delete_entry_command(switch, table_name, handle_id, thrift_port=9030):
    p4_command_prefix = "echo \"table_modify"
    p4_command_args = [p4_command_prefix, table_name, handle_id] + ["\""]
    p4_run_command = "simple_switch_CLI --thrift-port " + str(thrift_port)
    p4_delete_command = " ".join(p4_command_args) + " | " + p4_run_command
    print("Executing P4 Delete Command:", p4_delete_command, "on Switch:", switch.get_name())
    stdout = switch.execute(p4_delete_command)
    print("Delete Command Result:", stdout)
        
def execute_p4_modify_entry_command(switch, table_name, action_name, handle_id, params, thrift_port=9030):
    p4_command_prefix = "echo \"table_modify"
    p4_command_args = [p4_command_prefix, table_name, action_name, handle_id] + params + ["\""]
    p4_run_command = "simple_switch_CLI --thrift-port " + str(thrift_port)
    p4_modify_command = " ".join(p4_command_args) + " | " + p4_run_command
    print("Executing P4 Modify Command:", p4_modify_command, "on Switch:", switch.get_name())
    stdout = switch.execute(p4_modify_command)
    print("Modify Command Result:", stdout)