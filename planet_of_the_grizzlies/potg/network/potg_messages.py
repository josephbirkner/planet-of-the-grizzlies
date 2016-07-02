
import json

class Message:

    mtype = ""
    payload = None

    def Parse(message):
        data = json.loads(message.decode('ascii'))
        return Message(data["type"], data["payload"])

    def __init__(self, mtype, payload):
        self.mtype = mtype
        self.payload = payload
        assert type(self.payload) == dict

    def to_bytes(self):
        return json.dumps({"type": self.mtype, "payload": self.payload}).encode("ascii")

    def value(self, key):
        return self.payload[key]


class ClientMessage(Message):

    def __init__(self, mtype, clientid, other_payload=None):
        if not other_payload:
            other_payload = {}
        other_payload["clientid"] = clientid
        super().__init__(mtype, other_payload)