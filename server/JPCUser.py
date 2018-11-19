from utl.jpc_parser.JPCProtocol import JPCProtocol
import time
import csv


class JPCUserList:
    def __init__(self, whitelist=None):
        self.users = []
        if whitelist:
            self.build_whitelist(whitelist)

    def build_whitelist(self, whitelist):
        with open(whitelist, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                name = row[0]
                mac = row[1]
                self.add(name, int(mac))

    def add(self, name, mac):
        user = JPCUser(name, mac)
        self.users.append(user)

    def establish(self, mac, socket):
        user = self.get_by_mac(mac)
        user.establish(socket)

    def get_by_name(self, name):
        for user in self.users:
            if str.lower(user.user) == str.lower(name):
                return user
        return None

    def get_by_mac(self, mac_address):
        for user in self.users:
            if user.mac_address == mac_address:
                return user
        return None

    def send_message(self, message_type, message, recipient):
        user = self.get_by_name(recipient)
        if user and user.connected:
            packet = JPCProtocol(JPCProtocol.TELL, {'message_type': message_type, 'recipient': recipient, 'message': message})
            user.send(packet)

    def update_heartbeat(self, mac):
        user = self.get_by_mac(mac)
        if user:
            user.update_heartbeat(time.time())
            return True
        else:
            return False

    def tx_rx_heartbeats(self):
        t = time.time()
        while True:
            n = time.time()
            if n - t >= JPCProtocol.HEARTBEAT_INTERVAL:
                t = n
                for user in self.users:
                    if user.connected:
                        JPCProtocol(JPCProtocol.HEARTBEAT).send(user.connection)
                        elapsed = t - user.last_heartbeat
                        if elapsed >= JPCProtocol.HEARTBEAT_TIMEOUT:
                            print('died')


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

