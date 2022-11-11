from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether
from scapy.sendrecv import send

# packet = IP()/TCP()
send(IP(src="192.190.1.1", dst="192.168.1.13")/TCP(sport=135,dport=135), count=2000)
