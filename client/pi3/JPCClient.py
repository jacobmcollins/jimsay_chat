import socket
from utl.jpc_parser.JPCProtocol import JPCProtocol
import time
import threading
import tkinter as tk


class JPCClient:
    def __init__(self, server_address):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((server_address, 27272))
        JPCProtocol(JPCProtocol.HELLO).send(self.server)

    def run(self):
        try:
            t = threading.Thread(target=self.send_heartbeats)
            t.start()
            running = True
            while running:
                data = self.server.recv(1024)
                if data:
                    data_list = JPCProtocol.decode(data)
                    for item in data_list:
                        running = self.process(item)
        except ConnectionResetError:
            print('Connection Reset')

    def send_heartbeats(self):
        t = time.time()
        while True:
            n = time.time()
            if n - t > 3:
                t = n
                self.send_heartbeat()

    def process(self, data):
        opcode = data['opcode']
        payload = data['payload']

        switcher = {
            JPCProtocol.TELL:       self.process_tell,
            JPCProtocol.ERROR:      self.process_error
        }

        return switcher[opcode](payload)

    def process_tell(self, payload):
        message = payload['message']
        print(message)
        return True

    def process_error(self, error_code):
        if error_code == JPCProtocol.ERROR_TIMED_OUT:
            self.close()
            return False
        return True

    def send(self, msg):
        JPCProtocol(JPCProtocol.SEND, msg).send(self.server)

    def receive(self):
        recv_data = self.server.recv(10000000)
        return recv_data

    def close(self):
        self.server.close()

    def send_heartbeat(self):
        JPCProtocol(JPCProtocol.HEARTBEAT).send(self.server)
