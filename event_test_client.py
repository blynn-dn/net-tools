import argparse
import hashlib
import hmac
import json
import logging

from http.client import HTTPConnection
import requests

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

HTTPConnection.debuglevel = 1  # everything but data
HTTPConnection.debuglevel = 2  # everything plus data


def main():
    default_url = 'http://localhost:8000/webhook/device'
    parser = argparse.ArgumentParser(description='webhook test client')
    parser.add_argument('-f', '--file', required=True, help='webhook JSON payload file')
    parser.add_argument('-s', '--secret', help='webhook secret key', required=True)
    parser.add_argument('--target', help=f"web hook target URL (default {default_url})", default=default_url)

    args = parser.parse_args()

    with open(args.file) as f:
        payload = json.load(f)

    # print(payload)

    encoded_payload = json.dumps(payload).encode('utf-8')
    hashed = hmac.new(args.secret.encode('utf-8'), encoded_payload, hashlib.sha512).hexdigest()
    headers = {
        'Content-Type': 'application/json',
        'X-Hook-Signature': hashed
    }

    # print(f'calling {args.target} with hash: {hashed}')
    r = requests.post(url=args.target, data=encoded_payload, headers=headers)
    print(r.status_code)
    #print(r.json())
    print(r.content)


if __name__ == '__main__':
    main()
