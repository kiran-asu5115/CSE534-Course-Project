import os
import random
import sys
import json

import flask
import requests

from config_paths import get_lib_config_path, get_project_config_path, get_slice_config_path
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for

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


def html_escape(text):
    html_escape_table = {
        "&amp;": "&",
        "&quot;": '"',
        "&apos;": "'",
        "&gt;": ">",
        "&lt;": "<",
    }
    return "".join(html_escape_table.get(c, c) for c in text)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/send_traffic', methods=["POST", "GET"])
def send_traffic():
    packet_type = request.form.get('packet_type')
    source = request.form.get('source_addr')
    dest = request.form.get('destination_addr')
    count = request.form.get('count')
    res = requests.post("http://%s:5080/send_traffic" % source, data={"packet_type": packet_type,
                                                                      "dest": dest,
                                                                      "source": source,
                                                                      "count": count})
    if res.status_code != 200:
        flash(message="Packets not sent %s" % dest, category="error")
    else:
        flash(message="Packet sent to %s" % dest, category="success")
    return redirect(url_for('home'))


@app.route('/send_junk_traffic', methods=["POST", "GET"])
def send_junk_traffic():
    packet_type = request.form.get('packet_type')
    source = request.form.get('source_addr')
    dest = "192.168.1.%s" % random.randint(5, 50)
    count = request.form.get('count')
    res = requests.post("http://%s:5080/send_traffic" % source, data={"packet_type": packet_type,
                                                                      "dest": dest,
                                                                      "source": source,
                                                                      "count": count})
    return redirect(url_for('home'))


@app.route('/sniff', methods=["POST", "GET"])
def sniff():
    packet_type = request.form.get('packet_type')
    source = request.form.get('source_addr')
    count = 10 if request.form.get('count') == "" else int(request.form.get('count'))
    res = requests.post("http://%s:5080/sniff_packet" % source, data={"packet_type": packet_type,
                                                                      "source": source,
                                                                      "count": count})
    if res.status_code not in [200, 302] or res.json()["packets"] == "":
        flash(message="No packects found", category="error")
    else:
        flash(message=html_escape(res.json()["packets"]), category="success")

    return redirect(url_for('home'))


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
