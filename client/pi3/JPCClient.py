import socket
from utl.jpc_parser.JPCProtocol import JPCProtocol


class JPCClient:
    def __init__(self, server_address):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((server_address, 27272))
        JPCProtocol(JPCProtocol.HELLO).send(self.server)

    def run(self):
        while True:
            data = self.server.recv(1024)
            if data:
                print(data)




    def send(self, msg):
        JPCProtocol(JPCProtocol.SEND, msg).send(self.server)

    def receive(self):
        recv_data = self.server.recv(10000000)
        return recv_data

    def close(self):
        self.server.close()

    def send_heartbeat(self):
        JPCProtocol(JPCProtocol.HEARTBEAT).send(self.server)
