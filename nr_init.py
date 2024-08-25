#!/usr/bin/env python3
# nr_init.py
import getpass
import logging
import os
from nornir import InitNornir

LOGGER = logging.getLogger(__name__)

def nr_init():

    # Init the Norn!
    nr = InitNornir(
        inventory={
            "plugin": "NautobotInventory",
            "options": {
                "nautobot_url": os.getenv("NAUTOBOT_URL"),
                "nautobot_token": os.getenv("NAUTBOT_TOKEN"),
                "filter_parameters": {"location": "Lab_A"},
                "ssl_verify": False,
            },
        },
    )

    # get creds from env variables if not set in inventory
    if nr.inventory.defaults.username == None:
        nr.inventory.defaults.username = os.getenv("NORNIR_USERNAME")

    if nr.inventory.defaults.password == None:
        nr.inventory.defaults.password = os.getenv("NORNIR_PASSWORD")

    return nr

if __name__ == "__main__":
    nr_init()
