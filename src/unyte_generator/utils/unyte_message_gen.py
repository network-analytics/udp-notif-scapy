import json
import pathlib
from datetime import datetime, timedelta


class Mock_payload_reader:

    def __init__(self) -> None:
        self.msg_payloads: dict = {}

    def __read_json(self, path) -> dict:
        if path in self.msg_payloads:
            now = datetime.now()
            msg_payload = self.msg_payloads[path]
            msg_payload['ietf-notification:notification']['eventTime'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            return self.msg_payloads[path]

        json_payload = None
        with open(path, 'r') as f:
            json_payload = json.load(f)

        self.msg_payloads[path] = json_payload

        return json_payload

    def get_json_push_update_notif(self, nb_payloads: int) -> list:
        json_mock_payload: dict = self.__read_json(str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/notifications/push-update.json')
        yang_push_msgs: list = []
        now = datetime.now()
        for i in range(nb_payloads):
            msg_timestamp = now - timedelta(minutes=(nb_payloads-i))
            json_mock_payload['ietf-notification:notification']['eventTime'] = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
            yang_push_msgs.append(json.dumps(json_mock_payload))
        return yang_push_msgs
