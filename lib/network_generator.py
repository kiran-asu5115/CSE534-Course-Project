import json
import socket
import logging

import psutil

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
from flask import Flask, jsonify, request

from cryptography.utils import  CryptographyDeprecationWarning

app = Flask(__name__)

warnings.simplefilter('ignore', CryptographyDeprecationWarning)

def gen_tcp_packet(dest, count=2000, iface="ens8"):
    ans, unans = sr(IP(dst=dest) / TCP(dport=[3000, 5000, 6000]), inter=0.1, retry=count, timeout=1, iface=iface)
    return ans, unans


def gen_udp_packet(dest, count=2000, iface="ens8"):
    ans, unans = sr(IP(dst=dest) / UDP(dport=[3000, 5000, 6000]), inter=0.1, retry=count, timeout=1, iface=iface)
    return ans, unans


def gen_icmp_packet(dest, count=2000, iface="ens8"):
    ans, unans = sr(IP(dst=dest) / ICMP(), inter=0.1, retry=count, timeout=1, iface=iface)
    return ans, unans


def sniff_packets(packet_type, intf="ens8", count=50):
    print("Sniffing at %s -- " % intf)
    packets = sniff(iface=intf, count=count)
    packets = sniff(offline=packets, filter=packet_type, prn=lambda x: x.summary(), count=count)
    return "<br><br>".join([packet.summary() for packet in packets])


def get_interface(ip_addr=None):
    if not ip_addr:
        ip_addr = socket.gethostbyname(socket.gethostname())
    nics = psutil.net_if_addrs()
    return [i for i in nics for j in nics[i] if j.address == ip_addr and j.family == socket.AF_INET][0]


@app.route("/send_traffic", methods=["POST"])
def update_content():
    packet_type = request.form.get('packet_type', None)
    dest = request.form.get('dest', None)
    count = int(request.form.get('count'))
    intf = get_interface()
    if packet_type.lower() == "icmp":
        ans, unans = gen_icmp_packet(dest, count, intf)
        print(ans, unans)
    elif packet_type.lower() == "udp":
        ans, unans = gen_udp_packet(dest, count, intf)
        print(ans, unans)
    else:
        ans, unans = gen_tcp_packet(dest, count, intf)
        print(ans, unans)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/sniff_packet", methods=["POST"])
def sniff_packet():
    packet_type = request.form.get('packet_type', None)
    src_ip = request.form.get('source_ip')
    count = int(request.form.get('count', 2))
    intf = get_interface(src_ip)
    sniffed_packets = sniff_packets(packet_type, intf, count)
    return json.dumps({'success': True, "packets": sniffed_packets}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret_101$'
    app.run(host="0.0.0.0", port=5080, debug=True)
