import json
import pathlib
from datetime import datetime, timedelta
from xml.dom import minidom


class Mock_payload_reader:

    def __init__(self) -> None:
        self.cached_msg_payloads: dict = {}

    def __read_json(self, path) -> dict:
        if path in self.cached_msg_payloads:
            return self.cached_msg_payloads[path]

        json_payload = None
        with open(path, 'r') as f:
            json_payload = json.load(f)

        self.cached_msg_payloads[path] = json_payload

        return json_payload

    def __read_xml(self, path) -> dict:
        if path in self.cached_msg_payloads:
            return self.cached_msg_payloads[path]

        xml_payload = minidom.parse(path)

        self.cached_msg_payloads[path] = xml_payload
        return xml_payload

    def get_xml_subscription_started_notif(self):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/xml/notifications/subscription-started.xml'
        xml_mock_payload: dict = self.__read_xml(path)
        now = datetime.now()
        root = xml_mock_payload.documentElement
        eventTime_nodes = root.getElementsByTagName('eventTime')
        first_eventTime_node = eventTime_nodes[0]
        first_eventTime_node.firstChild.data = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        return root.toxml()

    def get_xml_push_update_notif(self, nb_payloads: int) -> list:
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/xml/notifications/push-update.xml'
        xml_mock_payload: dict = self.__read_xml(path)
        yang_push_msgs: list = []
        now = datetime.now()
        for i in range(nb_payloads):
            msg_timestamp = now - timedelta(minutes=(nb_payloads-i))
            root = xml_mock_payload.documentElement
            eventTime_nodes = root.getElementsByTagName('eventTime')
            first_eventTime_node = eventTime_nodes[0]
            first_eventTime_node.firstChild.data = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
            yang_push_msgs.append(root.toxml())
        return yang_push_msgs

    def get_xml_subscription_terminated_notif(self):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/xml/notifications/subscription-terminated.xml'
        xml_mock_payload: dict = self.__read_xml(path)
        now = datetime.now()
        root = xml_mock_payload.documentElement
        eventTime_nodes = root.getElementsByTagName('eventTime')
        first_eventTime_node = eventTime_nodes[0]
        first_eventTime_node.firstChild.data = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        return root.toxml()

    def get_json_subscription_started_notif(self):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/notifications/subscription-started.json'
        json_mock_payload: dict = self.__read_json(path)
        now = datetime.now()
        json_mock_payload['ietf-notification:notification']['eventTime'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        return json.dumps(json_mock_payload)

    def get_json_subscription_modified_notif(self):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/notifications/subscription-modified.json'
        json_mock_payload: dict = self.__read_json(path)
        now = datetime.now()
        json_mock_payload['ietf-notification:notification']['eventTime'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        return json.dumps(json_mock_payload)

    def get_json_subscription_terminated_notif(self):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/notifications/subscription-terminated.json'
        json_mock_payload: dict = self.__read_json(path)
        now = datetime.now()
        json_mock_payload['ietf-notification:notification']['eventTime'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        return json.dumps(json_mock_payload)

    def get_json_push_update_notif(self, nb_payloads: int) -> list:
        json_mock_payload: dict = self.__read_json(str(pathlib.Path(__file__).parent.parent.parent.absolute()
                                                       ) + '/resources/json/notifications/push-update.json')
        yang_push_msgs: list = []
        now = datetime.now()
        for i in range(nb_payloads):
            msg_timestamp = now - timedelta(minutes=(nb_payloads-i))
            json_mock_payload['ietf-notification:notification']['eventTime'] = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
            yang_push_msgs.append(json.dumps(json_mock_payload))
        return yang_push_msgs
