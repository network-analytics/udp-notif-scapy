import json
import pathlib


class Mock_payload_reader:

    def read_json(self, path):
        json_message = json.dumps(open(path, 'r').read())
        return json.loads(json_message)

    def generate_message(self, message_size):
        if message_size == "small":
            return self.read_json(str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/small.json')
        elif message_size == "big":
            return self.read_json(str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/big.json')
