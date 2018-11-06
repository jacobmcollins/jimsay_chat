import socket
from utl.jpc_parser.JPCProtocol import JPCProtocol


class JPCClient:
    def __init__(self, server_address):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_address, 27272))
        json_data = JPCProtocol(JPCProtocol.HELLO, '').to_json()
        self.s.send(json_data.encode())

    def send(self, msg):
        json_data = JPCProtocol(JPCProtocol.SEND, msg).to_json()
        self.s.send(json_data.encode())

    def receive(self):
        recv_data = self.s.recv(10000000)
        return recv_data

    def close(self):
        self.s.close()
