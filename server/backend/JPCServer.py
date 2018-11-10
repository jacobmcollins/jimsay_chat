import socket
import json
from utl.jpc_parser.JPCProtocol import JPCProtocol
import csv
import select
import sys
import queue


class JPCServer:
    def __init__(self):
        self.whitelist = {}
        self.build_whitelist()
        print(self.whitelist)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 27272))

    def build_whitelist(self):
        with open("pi_whitelist.txt", "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.whitelist[row[0]] = int(row[1])

    def run(self):
        self.s.listen(5)
        inputs = [self.s]
        outputs = []
        message_queues = {}

        while inputs:
            readable, writable, exceptional = select.select(
                inputs, outputs, inputs)
            for s in readable:
                if s is self.s:
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    inputs.append(connection)
                    message_queues[connection] = queue.Queue()
                else:
                    data = s.recv(1024)
                    if data:
                        # self.process(data)
                        print(data)
                        message_queues[s].put(data)
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del message_queues[s]

            for s in writable:
                try:
                    next_msg = message_queues[s].get_nowait()
                except queue.Empty:
                    outputs.remove(s)
                else:
                    s.send(next_msg)

            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del message_queues[s]

    def process(self, data):
        opcode = data['opcode']
        mac_address = data['mac_address']
        payload = data['payload']
        in_whitelist = False

        for key, value in self.whitelist.items():
            if mac_address == value:
                in_whitelist = True

        if not in_whitelist:
            return JPCProtocol.ERROR_ILLEGAL_NAME

        switcher = {
            JPCProtocol.HELLO:      self.process_hello,
            JPCProtocol.HEARTBEAT:  self.process_heartbeat,
            JPCProtocol.SEND:       self.process_send,
            JPCProtocol.TELL:       self.process_tell,
            JPCProtocol.ERROR:      self.process_error
        }

        switcher[opcode](payload)

    def process_hello(self, payload):
        print('hello')

    def process_heartbeat(self, payload):
        print('heartbeat')

    def process_send(self, payload):
        print('send')

    def process_tell(self, payload):
        print('tell')

    def process_error(self, payload):
        print('error')

    def process_none(self, payload):
        print('else')

