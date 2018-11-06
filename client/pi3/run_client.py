import socket
from utl.jpc_parser.jpc_protocol import JPCProtocol


class JPCClient:
    def __init__(self, server_address):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_address, 50001))

    def send(self, msg):
        json_data = JPCProtocol(msg).to_json()
        self.s.send(json_data.encode())

    def receive(self):
        recv_data = self.s.recv(10000000)
        return recv_data

    def close(self):
        self.s.close()


if __name__ == '__main__':
    client = JPCClient('192.168.0.14')
    client.send('abcdefgh')
    data = client.receive()
    print(data.decode())
    print('received', len(data), 'bytes')
    client.close()
