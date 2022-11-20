import os
import random
import sys
import json

import requests

from config_paths import get_lib_config_path, get_project_config_path, get_slice_config_path
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

lib_config_path = get_lib_config_path()
sys.path.insert(0, lib_config_path)


def set_environ(filename):
    with open(filename, "r+") as fp:
        data = json.load(fp)
    for key, value in data.items():
        os.environ[key] = value


project_config_path = get_project_config_path()
set_environ(project_config_path)

from lib.slice_builder import MeasurementSlice
from lib.setup_elk_grafana import Instrumentize


def read_config(filename):
    with open(filename, "r+") as fp:
        data = json.load(fp)
    return data


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/send_traffic', method=["POST", "GET"])
def home():
    packet_type = request.form.get('packet_type')
    source = request.form.get('source')
    dest = request.form.get('dest')
    count = request.form.get('count')
    res = requests.get("http://%s:5080/send_traffic" % source, data={"packet_type": packet_type,
                                                                     "dest": dest,
                                                                     "count": count})
    return render_template("home.html")


@app.route('/send_junk_traffic', method=["POST", "GET"])
def home():
    packet_type = request.form.get('packet_type')
    source = request.form.get('source')
    dest = "192.168.1.%s" % random.randint(5,50)
    count = request.form.get('count')
    res = requests.get("http://%s:5080/send_traffic" % source, data={"packet_type": packet_type,
                                                                     "dest": dest,
                                                                     "count": count})
    return render_template("home.html")

@app.route('/sniff', method=["POST", "GET"])
def home():
    packet_type = request.form.get('packet_type')
    source = request.form.get('source')
    intf = request.form.get('intf')
    res = requests.get("http://%s:5080/send_traffic" % source, data={"packet_type": packet_type,
                                                                     "intf": intf})
    return render_template("home.html")

def main():
    slice_config_file_name = "final_topo_slice_config.json"
    slice_config_path = get_slice_config_path(file_name=slice_config_file_name)
    slice_config = read_config(slice_config_path)
    s = MeasurementSlice(slice_config)
    s.create_slice()
    s.get_slice_ssh_commands()
    s.configure_ips()
    s.add_config_files_to_slice_nodes()

    inst_slice = Instrumentize(slice_config["slice_name"])
    app.config['SECRET_KEY'] = 'secret_101$'
    app.run(host="0.0.0.0", port=5081, debug=True)


if __name__ == '__main__':
    main()
