from uuid import getnode as get_mac
import json


class JPCProtocol:
    # opcodes
    ERROR = 0x10000001
    HEARTBEAT = 0x10000002
    HELLO = 0x10000003
    SEND = 0x10000001
    TELL = 0x10000002

    # error codes
    ERROR_UNKNOWN = 0x20000001
    ERROR_ILLEGAL_OPCODE = 0x20000002
    ERROR_ILLEGAL_LENGTH = 0x20000003
    ERROR_WRONG_VERSION = 0x20000004
    ERROR_NAME_EXISTS = 0x20000005
    ERROR_ILLEGAL_NAME = 0x20000006
    ERROR_ILLEGAL_MESSAGE = 0x20000007

    def __init__(self, opcode, message=None, mac_address=get_mac()):
        self.opcode = opcode
        self.message = message
        self.mac_address = mac_address

    def to_json(self):
        js = {
            'opcode':      self.opcode,
            'mac_address': self.mac_address,
            'payload':     None
        }

        if self.opcode == JPCProtocol.SEND:
            js['payload'] = self.message

        return json.dumps(js)
