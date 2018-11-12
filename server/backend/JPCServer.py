import csv
import json
import threading
import time
import socket
import string

from server.backend.JPCUser import JPCUser
from utl.jpc_parser.JPCProtocol import JPCProtocol


class JPCServer:
    def __init__(self):
        self.users = []
        self.build_whitelist()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 27272))

    def send_message(self, messageData, messageRecipient, messageLength):
        # do some encryption
        encrypted = self.shift_string(messageData, messageLength)
        print(encrypted)
        decrypted = self.shift_string(messageData, messageLength*-1)
        print(decrypted)
        """self.process_send(messageRecipient, messageData)"""

    def shift_string(my_string, shift):
        alph_string = string.ascii_letters # string of both uppercase/lowercase letters
        return ''.join([chr(ord(c)+shift) if c in alph_string else c for c in my_string])

    def build_whitelist(self):
        with open("pi_whitelist.txt", "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                name = row[0]
                mac = row[1]
                self.users.append(JPCUser(name, int(mac)))

    def run(self):
        self.s.listen(5)
        threading.Thread(target=self.check_heartbeats).start()
        while True:
            connection, client_address = self.s.accept()
            print(connection)
            print(client_address)
            threading.Thread(target=self.handle, args=[connection]).start()

    def handle(self, connection):
        running = True
        try:
            while running:
                data = connection.recv(1024)
                if data:
                    data_list = JPCProtocol.decode(data)
                    for json_data in data_list:
                        print(json_data)
                        self.process(json.loads(json_data), connection)
        except ConnectionAbortedError:
            print('Connection Aborted')

    def check_heartbeats(self):
        while True:
            for user in self.users:
                now = time.time()
                if user.connected:
                    elapsed = now - user.last_heartbeat
                    if elapsed > 5:
                        print('died')
                        user.close(JPCProtocol.ERROR_TIMED_OUT)

    def process(self, data, connection):
        opcode = data['opcode']
        payload = data['payload']

        switcher = {
            JPCProtocol.HELLO:      self.process_hello,
            JPCProtocol.HEARTBEAT:  self.process_heartbeat,
            #JPCProtocol.SEND:       self.process_send,
            #JPCProtocol.TELL:       self.process_tell,
            #JPCProtocol.ERROR:      self.process_error
        }

        switcher[opcode](payload, connection)

    def get_user_by_mac(self, mac_address):
        for item in self.users:
            if item.mac_address == mac_address:
                return item
        return None

    def process_hello(self, payload, s):
        x = self.get_user_by_mac(payload)
        if x:
            print('hello')
            x.establish(s)
            x.update_heartbeat(time.time())
        else:
            return JPCProtocol.ERROR_ILLEGAL_NAME

    def process_heartbeat(self, payload, s):
        x = self.get_user_by_mac(payload)
        if x:
            print('heartbeat')
            x.update_heartbeat(time.time())
        else:
            return JPCProtocol.ERROR_ILLEGAL_NAME

    def process_send(self, payload):
        print('send')

    def process_tell(self, payload):
        print('tell')

    def process_error(self, payload):
        print('error')

    def process_none(self, payload):
        print('else')

    def send_message(self, user, msg):
        packet = JPCProtocol(JPCProtocol.SEND, msg).encode()
        self.name_to_socket[user].send(packet)


