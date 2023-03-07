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

    ####################################################### XML #######################################################

    def get_xml_subscription_started_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/xml/notifications/subscription-started.xml'
        xml_mock_payload: dict = self.__read_xml(path)
        root = xml_mock_payload.documentElement
        # Setting eventTime
        eventTime_nodes = root.getElementsByTagName('eventTime')
        first_eventTime_node = eventTime_nodes[0]
        first_eventTime_node.firstChild.data = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        # Setting sequenceNumber
        seq_number_nodes = root.getElementsByTagName('sequenceNumber')
        seq_number_nodes[0].firstChild.data = sequence_number
        return root.toxml()

    def get_xml_subscription_modified_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/xml/notifications/subscription-modified.xml'
        xml_mock_payload: dict = self.__read_xml(path)
        root = xml_mock_payload.documentElement
        eventTime_nodes = root.getElementsByTagName('eventTime')
        first_eventTime_node = eventTime_nodes[0]
        first_eventTime_node.firstChild.data = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        # Setting sequenceNumber
        seq_number_nodes = root.getElementsByTagName('sequenceNumber')
        seq_number_nodes[0].firstChild.data = sequence_number
        return root.toxml()

    def get_xml_subscription_terminated_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/xml/notifications/subscription-terminated.xml'
        xml_mock_payload: dict = self.__read_xml(path)
        root = xml_mock_payload.documentElement
        eventTime_nodes = root.getElementsByTagName('eventTime')
        first_eventTime_node = eventTime_nodes[0]
        first_eventTime_node.firstChild.data = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        # Setting sequenceNumber
        seq_number_nodes = root.getElementsByTagName('sequenceNumber')
        seq_number_nodes[0].firstChild.data = sequence_number
        return root.toxml()

    def get_xml_push_update_1_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0) -> list:
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/xml/notifications/push-update-1.xml'
        xml_mock_payload: dict = self.__read_xml(path)
        root = xml_mock_payload.documentElement
        eventTime_nodes = root.getElementsByTagName('eventTime')
        first_eventTime_node = eventTime_nodes[0]
        first_eventTime_node.firstChild.data = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        # Setting sequenceNumber
        seq_number_nodes = root.getElementsByTagName('sequenceNumber')
        seq_number_nodes[0].firstChild.data = sequence_number
        return root.toxml()

    def get_xml_push_update_2_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0) -> list:
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/xml/notifications/push-update-2.xml'
        xml_mock_payload: dict = self.__read_xml(path)
        root = xml_mock_payload.documentElement
        eventTime_nodes = root.getElementsByTagName('eventTime')
        first_eventTime_node = eventTime_nodes[0]
        first_eventTime_node.firstChild.data = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        # Setting sequenceNumber
        seq_number_nodes = root.getElementsByTagName('sequenceNumber')
        seq_number_nodes[0].firstChild.data = sequence_number
        return root.toxml()
    
    ####################################################### JSON #######################################################

    def get_json_subscription_started_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/notifications/subscription-started.json'
        json_mock_payload: dict = self.__read_json(path)
        json_mock_payload['ietf-notification:notification']['eventTime'] = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        json_mock_payload['ietf-notification:notification']['ietf-notification-sequencing:sequenceNumber'] = sequence_number
        return json.dumps(json_mock_payload)

    def get_json_subscription_modified_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/notifications/subscription-modified.json'
        json_mock_payload: dict = self.__read_json(path)
        json_mock_payload['ietf-notification:notification']['eventTime'] = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        json_mock_payload['ietf-notification:notification']['ietf-notification-sequencing:sequenceNumber'] = sequence_number
        return json.dumps(json_mock_payload)

    def get_json_subscription_terminated_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0):
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/notifications/subscription-terminated.json'
        json_mock_payload: dict = self.__read_json(path)
        json_mock_payload['ietf-notification:notification']['eventTime'] = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        json_mock_payload['ietf-notification:notification']['ietf-notification-sequencing:sequenceNumber'] = sequence_number
        return json.dumps(json_mock_payload)

    def get_json_push_update_1_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0) -> list:
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/notifications/push-update-1.json'
        json_mock_payload: dict = self.__read_json(path)
        json_mock_payload['ietf-notification:notification']['eventTime'] = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        json_mock_payload['ietf-notification:notification']['ietf-notification-sequencing:sequenceNumber'] = sequence_number
        return json.dumps(json_mock_payload)

    def get_json_push_update_2_notif(self, msg_timestamp: datetime = datetime.now(), sequence_number: int = 0) -> list:
        path = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/resources/json/notifications/push-update-2.json'
        json_mock_payload: dict = self.__read_json(path)
        json_mock_payload['ietf-notification:notification']['eventTime'] = msg_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        json_mock_payload['ietf-notification:notification']['ietf-notification-sequencing:sequenceNumber'] = sequence_number
        return json.dumps(json_mock_payload)
