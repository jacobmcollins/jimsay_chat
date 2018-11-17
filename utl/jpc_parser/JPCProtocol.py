from uuid import getnode as get_mac
import json
import crc16


class JPCProtocol:
    # opcodes
    HELLO = 0
    CLOSE = 1
    HEARTBEAT = 2
    ERROR = 3
    SEND = 4
    TELL = 5

    # error codes
    ERROR_UNKNOWN = 0
    ERROR_TIMED_OUT = 1

    # misc
    HEARTBEAT_INTERVAL = 1
    HEARTBEAT_TIMEOUT = 5
    STANDARD_PORT = 27272

    def __init__(self, opcode, payload=None):
        self.opcode = opcode
        self.payload = payload

    def to_json(self):
        js = {
            'opcode':      self.opcode,
            'payload':     self.payload
        }

        if self.opcode == JPCProtocol.SEND:
            js['payload'] = self.payload
        elif self.opcode == JPCProtocol.HELLO:
            js['payload'] = get_mac()
        elif self.opcode == JPCProtocol.HEARTBEAT:
            js['payload'] = get_mac()

        return json.dumps(js)

    def encode(self):
        data = self.to_json().encode()
        crc = crc16.crc16xmodem(data).to_bytes(length=2, byteorder='little')
        data += crc
        raw_data = bytes([])
        end = bytes([0x7E])
        for byte in data:
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
                    crc = crc16.crc16xmodem(data[:-2]).to_bytes(length=2, byteorder='little')
                    if crc == data[-2:]:
                        data_array.append(json.loads(data[:-2].decode()))
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
