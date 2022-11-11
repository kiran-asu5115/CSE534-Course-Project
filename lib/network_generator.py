from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether
from scapy.sendrecv import send


class NetworkGen:
    def __init__(self):
        # packet = IP()/TCP()
        send(IP(src="192.190.1.1", dst="192.190.1.2")/TCP(sport=135,dport=135), count=2000)

n = NetworkGen()

