import json
import random


class mock_message_generator:

    def read_json(self, path):
        json_message = json.dumps(open(path, 'r').read())
        return json.loads(json_message)

    def generate_ordered_ints(self):
        message = "0123456789"
        for _ in range(6):
            message += message
        return message

    def generate_random_ints(self):
        message = "0123456789"
        for _ in range(random.randint(6, 12)):
            message += message
        return message

    def generate_message(self, message_type='ints'):
        if message_type == "json":
            return self.read_json("./message.json")
        elif message_type == "ints":
            return self.generate_ordered_ints()
        elif message_type == "rand":
            return self.generate_random_ints()
