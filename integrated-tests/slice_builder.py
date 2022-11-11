from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager


def read_config(filename):
    return None


class SetupSlice:
    def __init__(self, filename):
        fablib = fablib_manager()
        # fablib.show_config()
        self.slice_config = read_config(filename)
        slice_name = "Kiran_Integrated_Test_1"
        print(f"Using slice {self.slice_name} at site {self.site}")

    def create_slice(self):
        try:
            print("Setting up slice...")
            # Create Slice
            self.slice = fablib.new_slice(name=self.slice_name)

            # Node1
            node1 = self.slice.add_node(name=node1_name, site=self.site)
            node1.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
            node1.set_image(self.default_image)
            iface1 = node1.add_component(model='NIC_Basic', name=node1_nic_name).get_interfaces()[0]

            # Node2
            node2 = self.slice.add_node(name=node2_name, site=self.site)
            node2.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
            node2.set_image(self.default_image)
            iface2 = node2.add_component(model='NIC_Basic', name=node2_nic_name).get_interfaces()[0]

            # Node3
            node3 = self.slice.add_node(name=node3_name, site=self.site)
            node3.set_capacities(cores=self.cores, ram=self.ram, disk=self.disk)
            node3.set_image(self.default_image)
            iface3 = node3.add_component(model='NIC_Basic', name=node3_nic_name).get_interfaces()[0]

            # Network
            net1 = self.slice.add_l2network(name=self.network_name, interfaces=[iface1, iface2, iface3])

            print("Slice setup done.")

        except Exception as e:
            print(f"Slice Fail: {e}")
            traceback.print_exc()
        try:
            # Submit Slice Request
            print("Submitting the new slice...")
            # slice.submit()
            self.slice.submit(wait_timeout=1000, wait_interval=60)
            print("Slice creation done.")

        except Exception as e:
            print(f"Slice Fail: {e}")
            traceback.print_exc()

    def get_slice_info(self):
        try:
            slice = fablib.get_slice(name=self.slice_name)
            for node in slice.get_nodes():
                print("Node:")
                print(f"   Name              : {node.get_name()}")
                print(f"   Cores             : {node.get_cores()}")
                print(f"   RAM               : {node.get_ram()}")
                print(f"   Disk              : {node.get_disk()}")
                print(f"   Image             : {node.get_image()}")
                print(f"   Image Type        : {node.get_image_type()}")
                print(f"   Host              : {node.get_host()}")
                print(f"   Site              : {node.get_site()}")
                print(f"   Management IP     : {node.get_management_ip()}")
                print(f"   Reservation ID    : {node.get_reservation_id()}")
                print(f"   Reservation State : {node.get_reservation_state()}")
                print(f"   SSH Command       : {node.get_ssh_command()}")
                print(f"   Components        :  ")
                for component in node.get_components():
                    print(f"      Name             : {component.get_name()}")
                    print(f"      Details          : {component.get_details()}")
                    print(f"      Disk (G)         : {component.get_disk()}")
                    print(f"      Units            : {component.get_unit()}")
                    print(f"      PCI Address      : {component.get_pci_addr()}")
                    print(f"      Model            : {component.get_model()}")
                    print(f"      Type             : {component.get_type()}")
                print(f"   Interfaces        :  ")
                for interface in node.get_interfaces():
                    print(f"       Name                : {interface.get_name()}")
                    print(f"           Bandwidth           : {interface.get_bandwidth()}")
                    print(f"           VLAN                : {interface.get_vlan()}")
                    print(f"           MAC                 : {interface.get_mac()}")
                    print(f"           OS iface name       : {interface.get_os_interface()}")
            for network in slice.get_l2networks():
                print("Network:")
                print(f"    Name:            {network.get_name()}")
            #print(f"Interface Map: {slice.get_interface_map()}")
        except Exception as e:
            print(f"Fail: {e}")
            traceback.print_exc()

    def extend_slice_lease(self):
        try:
            slice = fablib.get_slice(name=self.slice_name)
            print(f"Lease End         : {slice.get_lease_end()}")

        except Exception as e:
            print(f"Exception: {e}")

        # Extend slice
        end_date = (datetime.datetime.now().astimezone() + datetime.timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S %z")

        try:
            slice = fablib.get_slice(name=self.slice_name)
            slice.renew(end_date)
        except Exception as e:
            print(f"Exception: {e}")

    def delete_slice(self):
        try:
            slice = fablib.get_slice(name=self.slice_name)
            slice.delete()
        except Exception as e:
            print(f"Fail: {e}")
            traceback.print_exc()
