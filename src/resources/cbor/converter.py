import cbor2
import glob
import json
from os.path import basename

CBOR_dir_output = "./notifications/"

json_notifications = [f for f in glob.glob("../json/notifications/*.json")]

print(json_notifications)

for json_notification_path in json_notifications:
  print("Converting " + json_notification_path)

  json_notification = None
  with open(json_notification_path, 'r') as f:
    json_notification = json.load(f)
  
  cbor_notification = cbor2.dumps(json_notification)
  output_cbor = CBOR_dir_output + basename(json_notification_path).replace('json', 'cbor')

  with open(output_cbor, 'wb') as fp:
    cbor2.dump(cbor_notification, fp)
