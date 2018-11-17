import socket
from utl.jpc_parser.JPCProtocol import JPCProtocol
import time
import threading


class JPCClient:
    def __init__(self, server_address):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((server_address, JPCProtocol.STANDARD_PORT))
        JPCProtocol(JPCProtocol.HELLO).send(self.server)

    def run(self):
        try:
            threading.Thread(target=self.send_heartbeats).start()
            running = True
            while running:
                data = self.server.recv(64000)
                print(data)
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
            if n - t >= JPCProtocol.HEARTBEAT_INTERVAL:
                t = n
                self.send_heartbeat()

    def process(self, data):
        print(data)
        opcode = data['opcode']
        payload = data['payload']

        switcher = {
            JPCProtocol.TELL:       self.process_tell,
            JPCProtocol.ERROR:      self.process_error,
            JPCProtocol.HEARTBEAT:   self.process_heartbeat
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

    def process_heartbeat(self, payload):
        print("heartbeat")
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
