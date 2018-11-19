import socket
import time
from utl.jpc_parser.JPCProtocol import JPCProtocol


class ReconnectingSocket:
    def __init__(self, server_address):
        self.address = server_address
        self.sock = None
        self.connected = False
        self.buffer = b''

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.sock.connect_ex((self.address, JPCProtocol.STANDARD_PORT)) != 0:
            time.sleep(1)
        self.connected = True

    def disconnect(self):
        if self.sock:
            self.sock.detach()
        self.sock = None
        self.connected = False

    def reconnect(self):
        self.disconnect()
        self.connect()

    def send(self, raw_data):
        if self.connected:
            self.sock.send(raw_data)

    def recv(self):
        if self.connected:
            data = self.sock.recv(1000000)
            data_list = JPCProtocol.decode(data)
            return data_list


if __name__ == '__main__':
    server = ReconnectingSocket()
    server.connect("localhost")
    JPCProtocol(JPCProtocol.HELLO).send(server.sock)
    while True:
        data = server.recv()
        if data:
            print(data)


