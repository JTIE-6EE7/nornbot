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

    # look for default creds in inventory
    if nr.inventory.defaults.username == None or nr.inventory.defaults.password == None:

        # look for creds in environment variables
        if os.getenv("NORNIR_USERNAME1") and os.getenv("NORNIR_PASSWORD"):
            nr.inventory.defaults.username = os.getenv("NORNIR_USERNAME")
            nr.inventory.defaults.password = os.getenv("NORNIR_PASSWORD")

        else:
            # prompt for creds
            nr.inventory.defaults.username = input("Username: ")
            nr.inventory.defaults.password = getpass.getpass()

    return nr


if __name__ == "__main__":
    nr_init()
