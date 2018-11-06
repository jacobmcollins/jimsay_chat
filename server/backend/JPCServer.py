import socket
import json
from utl.jpc_parser.JPCProtocol import JPCProtocol


class JPCServer:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 27272))
        self.users = {}

    def run(self):
        self.s.listen(1)
        running = True
        while running:
            conn, addr = self.s.accept()
            print('Client is at {}'.format(addr))
            data = conn.recv(1000000)
            js = json.loads(data.decode())
            self.process(js)
            conn.close()

    def process(self, data):
        mac_address = data['mac_address']
        opcode = data['opcode']
        message = data['message']

        switcher = {
            JPCProtocol.HELLO:     self.process_hello,
            JPCProtocol.HEARTBEAT: self.process_heartbeat,
            JPCProtocol.SEND:      self.process_send,
            JPCProtocol.TELL:      self.process_tell,
            JPCProtocol.ERROR:     self.process_error,
        }

        func = switcher.get(opcode, lambda: self.process_none())
        func(mac_address, message)

    def process_hello(self, mac_address, username):
        self.users[mac_address] = username
        print('hello')
        print(username)
        print(mac_address)

    def process_heartbeat(self, mac_address, username):
        print('heartbeat')

    def process_send(self, mac_address, username):
        print('send')

    def process_tell(self, mac_address, username):
        print('tell')

    def process_error(self, mac_address, username):
        print('error')

    def process_none(self, mac_address, username):
        print('else')

