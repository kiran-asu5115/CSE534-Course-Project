from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
import socket
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/send_traffic", methods=["POST"])
def update_content():

    return jsonify({'packets_sent': ""})
@app.route("/send_junk_traffic", methods=["POST"])
def update_content():

    return jsonify({'packets_sent': ""})

class NetworkGen:
    def __init__(self, client_port=5081, server_port=5080):
        self.server_port = server_port
        pass

    def gen_tcp_packet(self, dest, count=2000, iface="ens8"):
        ans, unans = sr(IP(dst=dest) / TCP(dport=[3000, 5000, 6000]), inter=0.1, retry=count, timeout=1, iface=iface)
        print(ans, unans)

    def gen_udp_packet(self, dest, count=2000, iface="ens8"):
        ans, unans = sr(IP(dst=dest) / UDP(dport=[3000, 5000, 6000]), inter=0.1, retry=count, timeout=1, iface=iface)
        print(ans, unans)

    def gen_icmp_packet(self, dest, count=2000, iface="ens8"):
        ans, unans = sr(IP(dst=dest) / ICMP(), inter=0.1, retry=count, timeout=1, iface=iface)
        print(ans, unans)

    def server(self, server_ip):
        # take the server name and port name
        host = server_ip
        port = 5000

        # create a socket at server side
        # using TCP / IP protocol
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the socket with server
        # and port number
        s.bind(('', port))

        # allow maximum 1 connection to
        # the socket
        s.listen(1)

        # wait till a client accept
        # connection
        c, addr = s.accept()

        # display client address
        print("CONNECTION FROM:", str(addr))

        # send message to the client after
        # encoding into binary string
        c.send(b"Reply from server")

        msg = "Bye.............."
        c.send(msg.encode())

        # disconnect the server
        c.close()

    def client(self,server_ip):
        # take the server name and port name
        host = server_ip
        port = 5000

        # create a socket at client side
        # using TCP / IP protocol
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM)

        # connect it to server and port
        # number on local computer.
        s.connect((host, port))

        # receive message string from
        # server, at a time 1024 B
        msg = s.recv(1024)

        # repeat as long as message
        # string are not empty
        while msg:
            print('Received:' + msg.decode())
            msg = s.recv(1024)

        # disconnect the client
        s.close()
    def start_server(self):

        app.config['SECRET_KEY'] = 'secret_101$'
        app.run(host="0.0.0.0", port=self.server_port, debug=True)


n = NetworkGen()
