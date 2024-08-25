#!/usr/bin/env python3
# nr_init.py
import getpass
import logging
import os
from nornir import InitNornir

LOGGER = logging.getLogger(__name__)


def nr_init(nb_location=None):
    # Init the Norn!
    nr = InitNornir(
        inventory={
            "plugin": "NautobotInventory",
            "options": {
                "nautobot_url": os.getenv("NAUTOBOT_URL"),
                "nautobot_token": os.getenv("NAUTBOT_TOKEN"),
                "filter_parameters": {"location": nb_location},
                "ssl_verify": False,
            },
        },
    )

    # get creds from env variables or prompts if not set in inventory
    if nr.inventory.defaults.username == None:
        if os.getenv("NORNIR_USERNAME"):
            nr.inventory.defaults.username = os.getenv("NORNIR_USERNAME")
        else:
            nr.inventory.defaults.username = input("Username: ")

    if nr.inventory.defaults.password == None:
        if os.getenv("NORNIR_PASSWORD"):
            nr.inventory.defaults.password = os.getenv("NORNIR_PASSWORD")
        else:
            nr.inventory.defaults.password = getpass.getpass()

    return nr


if __name__ == "__main__":
    nr_init()
