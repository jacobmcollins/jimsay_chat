import threading
import socket
from server.JPCUser import JPCUserList
from utl.jpc_parser.JPCProtocol import JPCProtocol


class JPCServer:
    def __init__(self):
        self.users = JPCUserList("pi_whitelist.txt")
        threading.Thread(target=self.users.tx_rx_heartbeats).start()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind(('', JPCProtocol.STANDARD_PORT))

    def send_message(self, message, recipient):
        self.users.send_message(message, recipient)

    def run(self):
        self.connection.listen(5)
        while True:
            connection, client_address = self.connection.accept()
            print(connection)
            print(client_address)
            threading.Thread(target=self.handle, args=[connection]).start()

    def handle(self, connection):
        running = True
        try:
            while running:
                data = connection.recv(64000)
                if data:
                    data_list = JPCProtocol.decode(data)
                    for json_data in data_list:
                        print(json_data)
                        self.process(json_data, connection)
        except:
            print('Connection Aborted')

    def process(self, data, connection):
        opcode = data['opcode']
        payload = data['payload']

        switcher = {
            JPCProtocol.HELLO:      self.process_hello,
            JPCProtocol.HEARTBEAT:  self.process_heartbeat,
        }

        switcher[opcode](payload, connection)

    def process_hello(self, payload, s):
        self.users.update_heartbeat(payload)
        self.users.establish(payload, s)

    def process_heartbeat(self, payload, s):
        self.users.update_heartbeat(payload)

