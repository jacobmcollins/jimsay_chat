import socket
from utl.jpc_parser.JPCProtocol import JPCProtocol


class JPCClient:
    def __init__(self, server_address):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_address, 27272))
        raw_data = JPCProtocol(JPCProtocol.HELLO).encode()
        self.s.send(raw_data)

    def send(self, msg):
        raw_data = JPCProtocol(JPCProtocol.SEND, msg).encode()
        self.s.send(raw_data)

    def receive(self):
        recv_data = self.s.recv(10000000)
        return recv_data

    def close(self):
        self.s.close()

    def send_heartbeat(self):
        heartbeat = JPCProtocol(JPCProtocol.HEARTBEAT).to_json()
        self.s.send(heartbeat.encode())
