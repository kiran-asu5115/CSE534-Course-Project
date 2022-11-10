import os

from fabrictestbed_extensions.mflib.mflib import mflib
from fabrictestbed_extensions.fablib.fablib import fablib
from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager



class SetupELK:
    def __init__(self, elk_port=10020):
        # The slice name of the slice with which you want to interact.
        self.slice_name = "Kiran_P4_Test_1"
        # self.mf.grafana_tunnel_local_port = elk_port


    def get_elk_info(self):
        # ELK SSH Tunnel Command
        print(self.mf.kibana_tunnel)

        # The ELK service was created by the mf.instrumentize call.
        # Get access info for Kibana by using the mflib.info call to the elk service.
        # Create a dictionary to pass to the service.
        data = {"get": ["nginx_id", "nginx_password"]}
        # Set the info you want to get.
        # Call info using service name and data dictionary.
        info_results = self.mf.info("elk", data)
        print(info_results)

        if info_results["success"]:
            print(f"user: {info_results['nginx_id']} \npass: {info_results['nginx_password']}")

    def upload_elk_dashboard(self):
        data = {"commands": []}

        # Add upload_dashboards command along with dashboard filenames to upload.
        data["commands"].append({"cmd": "upload_dashboards", "dashboard_filenames": ["FABRICDashboards.ndjson"]})

        # Add add_dashboards command along with dashboard filenames to add.
        data["commands"].append({"cmd": "add_dashboards", "dashboard_filenames": ["FABRICDashboards.ndjson"]})

        # Add list of files to upload to the Measurement Node.
        files = ["./dashboard_examples/kibana/FABRICDashboards.ndjson"]

        # Call update
        results = self.mf.update("elk", data, files)
        print(results)

        # Array to be filled with full paths of all dashboard files in dashboards_folder directory
        dashboard_filenames = []
        dashboards_folder = "./dashboard_examples/kibana/"

        # Loop through dashboards folder
        for file in os.listdir(dashboards_folder):
            # Only upload dashboard files
            if file.endswith(".ndjson"):
                # Add full path of dashboard to array
                dashboard_filenames.append(os.path.join(dashboards_folder, file))

        # Build update command.
        data = {"commands": []}

        # Add upload_dashboards command along with dashboard filenames to upload.
        data["commands"].append({"cmd": "upload_dashboards", "dashboard_filenames": dashboard_filenames})

        # Add add_dashboards command along with dashboard filenames to add.
        data["commands"].append({"cmd": "add_dashboards", "dashboard_filenames": dashboard_filenames})

        # Call update
        dashboard_results = self.mf.update("elk", data, dashboard_filenames)
        print(dashboard_results)

    def get_node_metric_link(self):
        # A few direct links to node data
        for node in self.mf.slice.get_nodes():
            if node.get_name() != "_meas_node":
                print(f"{node.get_name()} ELK Metric Overview")
                print(
                    f"    http://localhost:10020/app/metrics/detail/host/{node.get_reservation_id()}-{node.get_name().lower()}")


class SetupGrafana:
    def __init__(self, port=10010):
        # The slice name of the slice with which you want to interact.
        self.slice_name = "Kiran_P4_Test_1"
        # self.mf.grafana_tunnel_local_port = port


    def get_grafana_info(self):
        # Grafana SSH Tunnel Command
        print(self.mf.grafana_tunnel)

        # The grafana_manager service was created by the mf.instrumentize call.
        # Get access info for Grafana by using the mflib.info call to the grafana_manager.
        # Create a dictionary to pass to the service.
        data = {"get": ["admin_password"]}
        # Set the info you want to get.
        # Call info using service name and data dictionary.
        info_results = self.mf.info("grafana_manager", data)
        print(info_results)

    def upload_grafana_dashboard(self):
        data = {"commands": []}
        data["commands"].append({"cmd": "upload_dashboards", "dashboard_filenames": ["up.json"]})
        data["commands"].append({"cmd": "add_dashboards", "dashboard_filenames": ["up.json"]})

        files = ["./dashboard_examples/grafana/up.json"]
        dashboard_results = self.mf.update("grafana_manager", data, files)
        print(dashboard_results)



class Instrumentize(SetupGrafana, SetupELK):
    def __init__(self):
        super().__init__()
        slice = fablib.get_slice(name=self.slice_name)
        self.setup_meas_node(slice)
        self.mf = mflib(self.slice_name)
        instrumetize_results = self.mf.instrumentize()
        self.get_grafana_info()
        self.get_elf_info()
        # self.slice = slice


    def setup_meas_node(self, slice):
        # Add measurement node to topology using static method.
        mflib.addMeasNode(slice)
        print("Done")

c = Instrumentize()
