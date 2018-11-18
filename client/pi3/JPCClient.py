import socket
from utl.jpc_parser.JPCProtocol import JPCProtocol
import time
import threading
from client.pi3.JPCClientGUI import JPCClientGUI


class JPCClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.server.connect_ex((self.server_address, JPCProtocol.STANDARD_PORT)) != 0:
            time.sleep(1)
        self.gui = JPCClientGUI()
        print(time.time())
        JPCProtocol(JPCProtocol.HELLO).send(self.server)
        self.send_heartbeat()
        threading.Thread(target=self.run).start()
        self.gui.run()

    def run(self):
        try:
            running = True
            t = time.time()
            while running:
                self.send_heartbeats(t)
                data = self.server.recv(64000)
                if data:
                    data_list = JPCProtocol.decode(data)
                    for item in data_list:
                        running = self.process(item)
        except ConnectionResetError:
            self.server.close()
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while self.server.connect_ex((self.server_address, JPCProtocol.STANDARD_PORT)) != 0:
                time.sleep(1)
            JPCProtocol(JPCProtocol.HELLO).send(self.server)
            self.send_heartbeat()
            self.run()

    def send_heartbeats(self, t):
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
        self.gui.set_message(message)
        return True

    def process_error(self, error_code):
        if error_code == JPCProtocol.ERROR_TIMED_OUT:
            self.close()
            return False
        return True

    def process_heartbeat(self, payload):
        return True

    def send(self, msg):
        JPCProtocol(JPCProtocol.SEND, msg).send(self.server)

    def receive(self):
        recv_data = self.server.recv(10000000)
        return recv_data

    def close(self):
        self.server.close()

    def send_heartbeat(self):
        print(time.time())
        JPCProtocol(JPCProtocol.HEARTBEAT).send(self.server)


