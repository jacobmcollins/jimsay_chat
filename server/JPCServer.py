import threading
import time
import socket
import string

from server.JPCUser import JPCUser, JPCUserList
from utl.jpc_parser.JPCProtocol import JPCProtocol


class JPCServer:
    def __init__(self):
        self.users = JPCUserList("pi_whitelist.txt")
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind(('', JPCProtocol.STANDARD_PORT))
        threading.Thread(target=self.send_heartbeats).start()

    def send_message(self, message, recipient):
        length = len(message)
        # do some encryption
        #encrypted = self.shift_string(message, length)
        #print(encrypted)
        #decrypted = self.shift_string(message, length*-1)
        #print(decrypted)
        self.users.send_message(message, recipient)

    def send_heartbeats(self):
        t = time.time()
        while True:
            n = time.time()
            if n - t > 3:
                t = n
                self.users.tx_rx_heartbeats()

    def shift_string(self, my_string, shift):
        alph_string = string.ascii_letters # string of both uppercase/lowercase letters
        return ''.join([chr(ord(c)+shift) if c in alph_string else c for c in my_string])

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
        except ConnectionAbortedError:
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
        x = self.users.get_by_mac(payload)

        if x:
            print('hello')
            x.establish(s)
            x.update_heartbeat(time.time())
        else:
            return JPCProtocol.ERROR_ILLEGAL_NAME

    def process_heartbeat(self, payload, s):
        self.users.update_heartbeat(payload)

