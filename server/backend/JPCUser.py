from utl.jpc_parser.JPCProtocol import JPCProtocol


class JPCUser:
    def __init__(self, user, mac_address):
        self.user = user
        self.mac_address = mac_address
        self.connection = None
        self.last_heartbeat = None
        self.connected = False

    def establish(self, connection):
        self.connection = connection
        self.connected = True

    def update_heartbeat(self, time):
        self.last_heartbeat = time

    def close(self, opcode=JPCProtocol.CLOSE, payload=None):
        JPCProtocol(opcode, payload).send(self.connection)
        self.connection.close()
        self.connection = None
        self.last_heartbeat = None
        self.connected = False

    def send(self, packet):
        if self.connected:
            packet.send(self.connection)

