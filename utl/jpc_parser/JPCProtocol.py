from uuid import getnode as get_mac
import json


class JPCProtocol:
    # opcodes
    ERROR = 0x10000001
    HEARTBEAT = 0x10000002
    HELLO = 0x10000003
    SEND = 0x10000004
    TELL = 0x10000005
    CLOSE = 0x10000006

    # error codes
    ERROR_UNKNOWN = 0x20000001
    ERROR_ILLEGAL_OPCODE = 0x20000002
    ERROR_ILLEGAL_LENGTH = 0x20000003
    ERROR_WRONG_VERSION = 0x20000004
    ERROR_NAME_EXISTS = 0x20000005
    ERROR_ILLEGAL_NAME = 0x20000006
    ERROR_ILLEGAL_MESSAGE = 0x20000007
    ERROR_TIMED_OUT = 0x20000008

    def __init__(self, opcode, message=None):
        self.opcode = opcode
        self.message = message

    def to_json(self):
        js = {
            'opcode':      self.opcode,
            'payload':     None
        }

        if self.opcode == JPCProtocol.SEND:
            js['payload'] = self.message
        elif self.opcode == JPCProtocol.HELLO:
            js['payload'] = get_mac()
        elif self.opcode == JPCProtocol.HEARTBEAT:
            js['payload'] = get_mac()

        return json.dumps(js)

    def encode(self):
        raw_data = bytes([])
        end = bytes([0x7E])
        for byte in self.to_json().encode():
            if byte == 0x7E or byte == 0x7D:
                raw_data += bytes([0x7D])
                raw_data += bytes([byte ^ 0x20])
            else:
                raw_data += bytes([byte])

        return end + raw_data + end

    def decode(raw_data):
        data_array = []
        data = b''
        i = 0
        while i < len(raw_data):
            byte = raw_data[i]
            if byte == 0x7E:
                if data != b'':
                    data_array.append(data.decode())
                    data = b''
            elif byte == 0x7D:
                i += 1
                byte = raw_data[i]
                data += bytes([byte ^ 0x20])
            else:
                data += bytes([byte])
            i += 1
        return data_array

    def send(self, sock):
        raw_data = self.encode()
        sock.send(raw_data)
