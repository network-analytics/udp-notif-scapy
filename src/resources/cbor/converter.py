import cbor2
import glob
import json
from os.path import basename

CBOR_dir_output = "./notifications/"

json_notifications = [f for f in glob.glob("../json/notifications/*.json")]

def change_encoding_cbor(json_notification: dict):
  for k,v in json_notification.items():
    if k == 'encoding' or k == 'ietf-subscribed-notifications:encoding':
      json_notification[k] = 'ietf-udp-notif-transport:encode-cbor'
    elif type(v) is dict:
      change_encoding_cbor(v)
    elif type(v) is list:
      for item in v:
        if type(item) is dict:
          change_encoding_cbor(item)


for json_notification_path in json_notifications:
  output_cbor = CBOR_dir_output + basename(json_notification_path).replace('json', 'cbor')
  print("Converting " + json_notification_path + " to " + output_cbor)

  json_notification = None
  with open(json_notification_path, 'r') as f:
    json_notification = json.load(f)

  change_encoding_cbor(json_notification=json_notification)

  cbor_notification = cbor2.dumps(json_notification)

  with open(output_cbor, 'wb') as fp:
    cbor2.dump(cbor_notification, fp)
