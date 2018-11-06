from uuid import getnode as get_mac
import json


class JPCProtocol:
    # opcodes
    ERROR = 0x12700001
    HEARTBEAT = 0x12700002
    HELLO = 0x12700003
    SEND = 0x12700011
    TELL = 0x12700012

    # error codes
    ERROR_UNKNOWN = 0x22700001
    ERROR_ILLEGAL_OPCODE = 0x22700002
    ERROR_ILLEGAL_LENGTH = 0x22700003
    ERROR_WRONG_VERSION = 0x22700004
    ERROR_NAME_EXISTS = 0x22700005
    ERROR_ILLEGAL_NAME = 0x22700006
    ERROR_ILLEGAL_MESSAGE = 0x22700007

    def __init__(self, opcode, message, mac_address=get_mac()):
        self.opcode = opcode
        self.message = message
        self.mac_address = mac_address

    def to_json(self):
        return json.dumps({
            'opcode': self.opcode,
            'mac_address': self.mac_address,
            'message': self.message
        })
