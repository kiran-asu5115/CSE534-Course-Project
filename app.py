import json
import random
import requests

from flask import Flask, jsonify, request, render_template, flash, redirect, url_for

from lib.get_data import GetMetrics

app = Flask(__name__)
g_m = GetMetrics()


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
    ip_map = {
        "192.168.1.2": "10.0.0.1",
        "192.168.2.2": "10.0.0.2",
        "192.168.3.2": "10.0.0.3",
        "192.168.4.2": "10.0.0.4"
    }
    packet_type = request.form.get('packet_type')
    source = request.form.get('source_addr')
    dest = request.form.get('destination_addr')
    count = request.form.get('count')
    res = requests.post("http://%s:5080/send_traffic" % ip_map[source], data={"packet_type": packet_type,
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
    ip_map = {
        "192.168.1.2": "10.0.0.1",
        "192.168.2.2": "10.0.0.2",
        "192.168.3.2": "10.0.0.3",
        "192.168.4.2": "10.0.0.4"
    }
    packet_type = request.form.get('packet_type')
    source = request.form.get('source_addr')
    count = 10 if request.form.get('count') == "" else int(request.form.get('count'))
    res = requests.post("http://%s:5080/sniff_packet" % ip_map[source], data={"packet_type": packet_type,
                                                                              "source": source,
                                                                              "count": count})
    if res.status_code not in [200, 302] or res.json()["packets"] == "":
        flash(message="No packects found", category="error")
    else:
        flash(message=html_escape(res.json()["packets"]), category="success")

    return redirect(url_for('home'))


@app.route('/get_metric', methods=["POST", "GET"])
def get_metrics():
    metric_name = request.form.get('metric_name')
    params = json.loads(request.form.get('params'))
    agg = None
    return json.dumps({'success': True, "metric_value": g_m.get_metric(metric_name, params, agg)}), 200, {
        'ContentType': 'application/json'}


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret_101$'
    app.run(host="0.0.0.0", port=5081, debug=True)
