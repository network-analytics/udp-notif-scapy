import json
import random
import pathlib


class mock_message_generator:

    def read_json(self, path):
        json_message = json.dumps(open(path, 'r').read())
        return json.loads(json_message)

    def generate_message(self, message_size):
        if message_size == "small":
            return self.read_json(str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/small.json')
        elif message_size == "big":
            return self.read_json(str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/big.json')
