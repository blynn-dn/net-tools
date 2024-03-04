# mock_data

Example using the test client: 
```shell
source ~/venv/bin/activate
python ./event_test_client.py -f /tmp/nb_event_updated_ip.json
...
<Response [200]>
```

Curl example: 

*Please not that this script is a work in progress as it appears that curl is not handling the payload 
in the same manner as the equivalent python logic.  Since the signature is a product of the payload, this example
is not working as expected*
```shell
sig=$(cat /tmp/nb_event_updated_ip.json | openssl dgst -sha512 -hmac "*****" | awk '{print "X-Hub-Signature: "$2}')
kkk --data "@/tmp/nb_event_updated_ip.json" \
 http://localhost:8082/v1/webhook/device

```

## netbox__event_device_created.json
A newly created device.  
* newly created device has event type `updated`
* snapshots.prechange is always None

## netbox_event_device_updated.json
An updated device.
* has event type `updated'
* snapshots.[pre|post]change are populated

## netbox_event_device_deleted.json
A deleted device.
* has event type `deleted`
* snapshots.prechange contains a copy of the deleted entity
* snapshots.postchange is always None