import traceback

from fablib_utils import slice_builder_utils, node_builder_utils, component_builder_utils, network_builder_utils
from fabrictestbed_extensions.fablib.fablib import FablibManager
from fabrictestbed_extensions.mflib.mflib import mflib


class SetupSlice:
    def __init__(self, config):
        self.fablib = FablibManager()
        self.slice_config = config
        self.slice_name = self.slice_config['slice_name']
        self.site = self.slice_config['site']
        print(f"Using slice {self.slice_name} at site {self.site}")
        self.integrated_slice = slice_builder_utils.create_slice(self.slice_name)

    # Create Slice
    def create_slice(self):
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

    def setup_meas_node(self):
        # Add measurement node to topology using static method.
        print("Setting up Measurement Node")
        mflib.addMeasNode(self.integrated_slice)
