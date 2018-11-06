from uuid import getnode as get_mac
import json


class JPCProtocol:
    def __init__(self, msg, mac=get_mac()):
        self.mac = mac
        self.msg = msg

    def to_json(self):
        return json.dumps({
            'mac': self.mac,
            'msg': self.msg
        })
