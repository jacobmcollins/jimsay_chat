import socket
from utl.jpc_parser.JPCProtocol import JPCProtocol


class JPCClient:
    def __init__(self, server_address):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_address, 27272))
        JPCProtocol(JPCProtocol.HELLO).send(self.s)

    def send(self, msg):
        JPCProtocol(JPCProtocol.SEND, msg).send(self.s)

    def receive(self):
        recv_data = self.s.recv(10000000)
        return recv_data

    def close(self):
        self.s.close()

    def send_heartbeat(self):
        JPCProtocol(JPCProtocol.HEARTBEAT).send(self.s)
