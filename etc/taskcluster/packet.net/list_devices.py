#!/usr/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import sys
import urllib.request


SERVO_PROJECT_ID = "e3d0d8be-9e4c-4d39-90af-38660eb70544"


def main():
    auth_token = os.environ.get("PACKET_AUTH_TOKEN")
    if not auth_token:
        sys.exit("$PACKET_AUTH_TOKEN is not set. See:\n"
                 "https://app.packet.net/projects/%s/settings/api-keys" % SERVO_PROJECT_ID)
    response = api_request(auth_token, "/projects/%s/devices?per_page=1000" % SERVO_PROJECT_ID)
    for device in response["devices"]:
        print(device["id"])
        print("  Host:\t" + device["hostname"])
        print("  Plan:\t" + device["plan"]["name"])
        print("  OS:\t" + device["operating_system"]["name"])
        for address in device["ip_addresses"]:
            if address["public"]:
                print("  IPv%s:\t%s" % (address["address_family"], address["address"]))
    assert response["meta"]["next"] is None


def api_request(auth_token, path, json_data=None, method=None):
    request = urllib.request.Request("https://api.packet.net" + path, method=method)
    request.add_header("X-Auth-Token", auth_token)
    if json_data is not None:
        request.add_header("Content-Type", "application/json")
        request.data = json.dumps(json_data)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


if __name__ == "__main__":
    main(*sys.argv[1:])
