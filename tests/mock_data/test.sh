# please not that this script is a work in progress -- it appears that `curl` is not handling the payload
# in the same manner as the equivalent python logic.  Since the signature is a product of the payload, this example
# is not working as expected
sig=$(cat nb_event_device_updated.json | openssl dgst -sha512 -hmac "XXab3de52310bfe623f2c3a1bef0f46b8b47f7zz" | awk '{print "X-Hub-Signature: "$2}')

echo "sig ${sig}"
curl -X POST -H "Content-Type: application/json" \
-H "${sig}" --data "@nb_event_device_updated.json" \
 http://localhost:8000/webhook/device
