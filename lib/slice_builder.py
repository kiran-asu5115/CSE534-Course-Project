import os
import traceback

from fabrictestbed_extensions.mflib.mflib import mflib
from fabrictestbed_extensions.fablib.fablib import FablibManager
from ipaddress import IPv4Network
from fablib_utils import slice_builder_utils, node_builder_utils, component_builder_utils, network_builder_utils


class MeasurementSlice:
    def __init__(self, config):
        self.fablib = FablibManager()
        self.slice_config = config
        self.slice_name = self.slice_config['slice_name']
        self.site = self.slice_config['site']
        print(f"Using slice {self.slice_name} at site {self.site}")
        self.integrated_slice = slice_builder_utils.create_slice(self.slice_name)
        

    # Create Slice
    def create_slice(self):
        slice = slice_builder_utils.get_slice_by_name_or_id(self.slice_name)
        if not slice:
            try:
                nic_comp = {}
                for node in self.slice_config["host_config"]:
                    node_params = {
                        "site": self.site,
                        "ram": node["ram"],
                        "disk": node["disk"],
                        "cores": node["cores"],
                        "image": node["image"]
                    }
                    node_comp = node_builder_utils.add_new_node(self.integrated_slice, node["hostname"], node_params)
                    for nic in node["host_nic"]:
                        node_nic = component_builder_utils.add_new_component(node_comp, comp_name=nic)
                        nic_comp[nic] = node_nic

                for conn in self.slice_config["conn_config"]:
                    conn_int = []
                    for interface in conn["interfaces"]:
                        conn_comp = component_builder_utils.get_interface_of_component(nic_comp[interface],
                                                                                       interface_number=1)
                        conn_int.append(conn_comp)
                    network_builder_utils.add_new_network_connection(self.integrated_slice, conn["name"],
                                                                     conn_interfaces=conn_int)

                print("Slice setup done.")

                # Adding Measuring Node
                self.setup_meas_node()

                # Submit Slice Request
                slice_builder_utils.submit_slice(self.integrated_slice)
                print("Slice creation done.")

                days = 14
                slice_builder_utils.extend_slice_lease(self.slice_name, days)

            except Exception as e:
                print(f"Slice Fail: {e}")
                traceback.print_exc()
    
    
    def add_config_files_to_slice_nodes(self):
        slice = self.get_slice_by_name_or_id()
        nodes = slice.get_nodes()
        for node in nodes:
            node_name = node.get_name()
            self.setup_node(node_name)
            self.setup_switch(node_name)
            print("Added Configuration Files to Node:", node_name)
    

    def setup_meas_node(self):
        # Add measurement node to topology using static method.
        print("Setting up Measurement Node")
        mflib.addMeasNode(self.integrated_slice)

    def delete_slice(self):
        slice_builder_utils.delete_slice(self.integrated_slice)

    def configure_ipv4_subnet(self, address_list):
        try:
            subnet = IPv4Network(address_list)
            available_ips = list(subnet)[1:]
        except Exception as e:
            print(f"Exception: {e}")
            return None, None
        return subnet, available_ips

    def get_slice_by_name_or_id(self, slice_id=None):
        if self.slice_name is None and slice_id is None:
            slice = None
        elif self.slice_name is not None:
            slice = self.fablib.get_slice(name=self.slice_name)
        else:
            slice = self.fablib.get_slice(slice_id=slice_id)
        return slice

    def get_slice_ssh_commands(self, slice_id=None):
        slice = self.get_slice_by_name_or_id(slice_id)
        nodes = slice.get_nodes()
        node_hostnames, node_ssh_commands = [], []
        ssh_config = os.environ["FABRIC_SSH_CONFIG"]
        private_key_file = os.environ["FABRIC_SLICE_PRIVATE_KEY_FILE"]
        ssh_command_prefix = "ssh -i " + private_key_file + " -F " + ssh_config + " "
        for node in nodes:
            try:
                node_username, node_management_ip = str(node.get_username()), str(node.get_management_ip())
                node_hostnames.append(node_username + "@" + node_management_ip)
                node_ssh_commands.append(ssh_command_prefix + node_hostnames[-1])
                print("Node {}:".format(len(node_hostnames)), node.get_name())
                print("Node Hostname:", node_hostnames[-1])
                print("SSH Access Command:", node_ssh_commands[-1])
            except Exception as e:
                print("Exception in Parsing Node Details:", node, e)

    def get_slice_components(self, slice_id=None):
        nodes = self.integrated_slice.get_nodes()
        for node in nodes:
            components = node.get_components()
            # print(vars(components[0]))
        return 

    def get_slice_interfaces(self, slice_id=None):
        slice = self.get_slice_by_name_or_id(slice_id)
        nodes = slice.get_nodes()
        interfaces = slice.get_interfaces()
        for interface in interfaces:
            interface_vals = vars(interface)
            print(interface_vals["network"])

    def configure_node_interface(self, node, network_name, subnet, available_ips):
        node_interface = node.get_interface(network_name=network_name)
        print("Node Interface:", node_interface)
        node_address = available_ips.pop(0)
        print("Node Address:", node_address, "for Node:", node.get_name())
        node_interface.ip_addr_add(addr=node_address, subnet=subnet)
        return node_address

    def unconfigure_node_interface(self, node, network_name, subnet, ip_address):
        node_interface = node.get_interface(network_name=network_name)
        print("Node Interface:", node_interface)
        node_interface.ip_addr_del(addr=ip_address, subnet=subnet)
        print("Deleted IP Address:", ip_address, "for Node:", node.get_name())

    def configure_ips(self):
        print("Configuring IPs for Networks in Slice")
        slice_components = self.get_slice_components()
        for conn in self.slice_config["conn_config"]:
            conn_name, conn_address_list = conn["name"], conn["address_list"]
            conn_hosts = []
            for conn_interface in conn["interfaces"]:
                for component in slice_components:
                    if component.get_name().endswith(conn_interface):
                        conn_hosts.append(component.get_node())
                        break
                    else:
                        pass
            if len(conn_hosts) == len(conn["interfaces"]):
                subnet, available_ips = self.configure_ipv4_subnet(address_list=conn_address_list)
                for conn_host in conn_hosts:
                    self.configure_node_interface(conn_host, conn_name, subnet, available_ips)
                print("Successfully Configured IP Addresses for:", conn)
            else:
                print("Adequate no. of Hosts not found for Connection:", conn, "needed", len(conn["interfaces"]), "got", len(conn_hosts))

    def upload_p4_program_file(self, switch_node, src_file_name, dst_file_name):
        p4_programs_directory = "p4_programs"
        try:
            src_file_path = os.path.join(os.getcwd(), "lib", p4_programs_directory, src_file_name)
            switch_node.upload_file(src_file_path, dst_file_name)
        except Exception as e:
            src_file_path = os.path.join(os.getcwd(), p4_programs_directory, src_file_name)
            switch_node.upload_file(src_file_path, dst_file_name)
            

    def upload_config_file(self, switch_node, src_file_name, dst_file_name):
        p4_config_directory = "host_configurations"
        try:
            src_file_path = os.path.join(os.getcwd(), "lib", p4_config_directory, src_file_name)
            switch_node.upload_file(src_file_path, dst_file_name)
        except Exception as e:
            src_file_path = os.path.join(os.getcwd(), p4_config_directory, src_file_name)
            switch_node.upload_file(src_file_path, dst_file_name)

    def get_node_by_name(self, slice, node_name):
        nodes = slice.get_nodes()
        switch_node = None
        for node in nodes:
            switch_node = node if node.get_name() == node_name else switch_node

        return switch_node

    def setup_switch(self, switch_node_name="s1"):
        p4_slice = self.get_slice_by_name_or_id()
        switch_node = self.get_node_by_name(p4_slice, node_name=switch_node_name)
        
        prog_file_name = "p4_basic_routing_2.p4"
        self.upload_p4_program_file(switch_node, prog_file_name, prog_file_name)
        
        config_file_name = "p4_switch_config.sh"
        self.upload_config_file(switch_node, config_file_name, config_file_name)
    
    def setup_node(self, node_name="s1"):
        p4_slice = self.get_slice_by_name_or_id()
        node = self.get_node_by_name(p4_slice, node_name=node_name)
        
        config_file_name = "general_node_config.sh"
        self.upload_config_file(node, config_file_name, config_file_name)
