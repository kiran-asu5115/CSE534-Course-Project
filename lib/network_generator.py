import json

from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
from flask import Flask, jsonify, request

app = Flask(__name__)


def gen_tcp_packet(dest, count=2000, iface="ens8"):
    ans, unans = sr(IP(dst=dest) / TCP(dport=[3000, 5000, 6000]), inter=0.1, retry=count, timeout=1, iface=iface)
    return ans, unans


def gen_udp_packet(dest, count=2000, iface="ens8"):
    ans, unans = sr(IP(dst=dest) / UDP(dport=[3000, 5000, 6000]), inter=0.1, retry=count, timeout=1, iface=iface)
    return ans, unans


def gen_icmp_packet(dest, count=2000, iface="ens8"):
    ans, unans = sr(IP(dst=dest) / ICMP(), inter=0.1, retry=count, timeout=1, iface=iface)
    return ans, unans


def sniff_packet(packet_type, intf):
    return True


@app.route("/send_traffic", methods=["POST"])
def update_content():
    packet_type = request.args.get('packet_type', None)
    dest = request.args.get('dest', None)
    count = int(request.args.get('count'))
    if packet_type == "ICMP":
        gen_icmp_packet(dest, count)
    elif packet_type == "UDP":
        gen_udp_packet(dest, count)
    else:
        gen_tcp_packet(dest, count)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/sniff_packet", method=["POST"])
def sniff():
    packet_type = request.args.get('packet_type', None)
    intf = request.args.get('intf')
    sniffed_packetss = sniff_packet(packet_type, intf)
    return json.dumps({'success': True, "packets": sniffed_packetss}), 200, {'ContentType': 'application/json'}


if "__name__" == "main":
    app.config['SECRET_KEY'] = 'secret_101$'
    app.run(host="0.0.0.0", port=5080, debug=True)
