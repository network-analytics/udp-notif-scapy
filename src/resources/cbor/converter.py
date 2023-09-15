import cbor2
import json


############ subscription-started ############
subscription_started_json = None
with open("../json/notifications/subscription-started.json", 'r') as f:
  subscription_started_json = json.load(f)

subscription_started_cbor = cbor2.dumps(subscription_started_json)

with open('./notifications/subscription-started.cbor', 'wb') as fp:
  cbor2.dump(subscription_started_cbor, fp)

############ subscription-started_with_anchor-time ############
subscription_started_with_anchor_time_json = None
with open("../json/notifications/subscription-started_with_anchor-time.json", 'r') as f:
  subscription_started_with_anchor_time_json = json.load(f)

subscription_started_with_anchor_time_cbor = cbor2.dumps(subscription_started_with_anchor_time_json)

with open('./notifications/subscription-started_with_anchor-time.cbor', 'wb') as fp:
  cbor2.dump(subscription_started_with_anchor_time_cbor, fp)


############ subscription-modified ############
subscription_modified_json = None
with open("../json/notifications/subscription-modified.json", 'r') as f:
  subscription_modified_json = json.load(f)

subscription_modified_cbor = cbor2.dumps(subscription_modified_json)

with open('./notifications/subscription-modified.cbor', 'wb') as fp:
  cbor2.dump(subscription_modified_cbor, fp)


############ subscription-terminated ############
subscription_terminated_json = None
with open("../json/notifications/subscription-terminated.json", 'r') as f:
  subscription_terminated_json = json.load(f)

subscription_terminated_cbor = cbor2.dumps(subscription_terminated_json)

with open('./notifications/subscription-terminated.cbor', 'wb') as fp:
  cbor2.dump(subscription_terminated_cbor, fp)


############ push-update-1 ############
push_update_1_json = None
with open("../json/notifications/push-update-1.json", 'r') as f:
  push_update_1_json = json.load(f)

push_update_1_cbor = cbor2.dumps(push_update_1_json)

with open('./notifications/push-update-1.cbor', 'wb') as fp:
  cbor2.dump(push_update_1_cbor, fp)


############ push-update-2 ############
push_update_2_json = None
with open("../json/notifications/push-update-2.json", 'r') as f:
  push_update_2_json = json.load(f)

push_update_2_cbor = cbor2.dumps(push_update_2_json)

with open('./notifications/push-update-2.cbor', 'wb') as fp:
  cbor2.dump(push_update_2_cbor, fp)


############ push-update-subscription ############
push_update_subscription_json = None
with open("../json/notifications/push-update-subscription.json", 'r') as f:
  push_update_subscription_json = json.load(f)

push_update_subscription_cbor = cbor2.dumps(push_update_subscription_json)

with open('./notifications/push-update-subscription.cbor', 'wb') as fp:
  cbor2.dump(push_update_subscription_cbor, fp)


############ push-update-subscription ############
push_update_subscription_json = None
with open("../json/notifications/push-update-subscription.json", 'r') as f:
  push_update_subscription_json = json.load(f)

push_update_subscription_cbor = cbor2.dumps(push_update_subscription_json)

with open('./notifications/push-update-subscription.cbor', 'wb') as fp:
  cbor2.dump(push_update_subscription_cbor, fp)


############ push-change-update-subscription ############
push_change_update_subscription_json = None
with open("../json/notifications/push-change-update-subscription.json", 'r') as f:
  push_change_update_subscription_json = json.load(f)

push_change_update_subscription_cbor = cbor2.dumps(push_change_update_subscription_json)

with open('./notifications/push-change-update-subscription.cbor', 'wb') as fp:
  cbor2.dump(push_change_update_subscription_cbor, fp)

