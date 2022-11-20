import os
import json
import base64
import warnings
import datetime
import subprocess

from prometheus_api_client import PrometheusConnect
from urllib3.exceptions import InsecureRequestWarning


class GetMetrics:
    def __init__(self):
        warnings.simplefilter('ignore', InsecureRequestWarning)
        self.exporter_password = None
        self.exporter_username = None
        self.username = None
        self.password = None
        if not self.get_credentials():
            raise Exception("Credentials not found")
        self.headers = self.create_auth_headers()
        # Instantiate a Prometheus client instance
        self.prom = PrometheusConnect(url="https://127.0.0.1:9090",
                                      headers=self.headers,
                                      disable_ssl=True)

    def create_auth_headers(self):
        cred = "%s:%s" % (self.username, self.password)
        cred = base64.b64encode(cred.encode())
        auth_header = {"Authorization": "Basic %s" % cred.decode()}
        return auth_header

    def get_credentials(self, filename="/home/mfuser/services/prometheus/extra_files/install_vars.json"):
        if os.path.exists(filename):
            output = json.loads(subprocess.getoutput("cat %s" % filename))
            self.username = output["fabric_prometheus_ht_user"]
            self.password = output["fabric_prometheus_ht_password"]
            self.exporter_username = output["node_exporter_username"]
            self.exporter_password = output["node_exporter_password"]
            return True
        print("Credential not found")
        return False

    def get_metric(self, metric, label=None, agg=None, delta_time=1):
        """

        :param metric: Metric name
        :param label: Labels for the metric
        :param agg: Aggregator function
        :param delta_time: Time range in minutes
        :return:
        """
        start_time = datetime.datetime.now() - datetime.timedelta(minutes=delta_time)
        end_time = datetime.datetime.now()
        if agg:
            if label:
                label_list = [str(key + "=" + "'" + label[key] + "'") for key in label]
                metric = metric + "{" + ",".join(label_list) + "}"
                metric = "%s(%s)" % (agg, metric)
            output = self.prom.custom_query_range(metric,start_time, end_time, step="60")

        else:
            output = self.prom.get_metric_range_data(metric, label_config=label, start_time=start_time,
                                                     end_time=end_time)
        return output["values"]


g = GetMetrics()
print(g.get_metric("node_network_receive_packets_total", {"instance": "Switch_1", "job": "node", "device": "ens10"},
             agg="count"))
