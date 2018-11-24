import socket
from utl.jpc_parser.JPCProtocol import JPCProtocol
import time
from client.pi3.JPCClientGUI import JPCClientGUI
from client.pi3.ReconnectingSocket import ReconnectingSocket


class JPCClient:
    def __init__(self, server_address):
        # Create GUI
        self.gui = JPCClientGUI()
        self.gui.start()

        # Create server connection
        self.server = ReconnectingSocket(server_address)
        self.server.connect()
        self.send_hello()
        self.send_heartbeat()

    def send_hello(self):
        print('tx: {} - {}'.format(time.time(), 'hello'))
        JPCProtocol(JPCProtocol.HELLO).send(self.server)

    def send_heartbeat(self):
        print('tx: {} - {}'.format(time.time(), 'hrtbt'))
        JPCProtocol(JPCProtocol.HEARTBEAT).send(self.server)

    def run(self):
        try:
            t = time.time()
            while True:
                self.process_packets()
                self.handle_heartbeats(t)
                self.gui.root.update()
                self.gui.root.update()
        except:
            self.re_run()

    def process_packets(self):
        try:
            data = self.server.recv()
            for item in data:
                print('rx: {} - {})'.format(time.time(), item))
                self.process(item)
        except:
            raise socket.error

    def handle_heartbeats(self, t):
        n = time.time()
        elapsed = n - t
        if self.server.connected and elapsed >= JPCProtocol.HEARTBEAT_INTERVAL:
            self.send_heartbeat()
            if elapsed >= JPCProtocol.HEARTBEAT_TIMEOUT:
                "died"

    def re_run(self):
        self.server.reconnect()
        self.send_hello()
        self.send_heartbeat()
        self.run()

    def process(self, data):
        opcode = data['opcode']
        payload = data['payload']

        switcher = {
            JPCProtocol.TELL:       self.process_tell,
            JPCProtocol.ERROR:      self.process_error,
            JPCProtocol.HEARTBEAT:   self.process_heartbeat
        }

        switcher[opcode](payload)

    def process_tell(self, payload):
        message = payload['message']
        message_type = payload['message_type']
        self.gui.set_message(message)

    def process_error(self, error_code):
        if error_code == JPCProtocol.ERROR_TIMED_OUT:
            self.close()
            return False

    def process_heartbeat(self, payload):
        pass

    def send(self, msg):
        JPCProtocol(JPCProtocol.SEND, msg).send(self.server)

    def close(self):
        self.server.close()



