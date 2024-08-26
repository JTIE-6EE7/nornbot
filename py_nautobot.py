#!/usr/bin/env python3

import os

import pynautobot

nautobot = pynautobot.api(
    url=os.getenv("NAUTOBOT_URL"),
    token=os.getenv("NAUTBOT_TOKEN"),
)

devices = nautobot.dcim.devices

print(devices)

switch = devices.get(name="n9k-dist-1")

print(switch.location)

print(dir(switch))
