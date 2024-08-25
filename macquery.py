#!/usr/bin/env python3
# macquery.py

import logging
import os
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from pprint import pprint as pp

# from nornir.core.task import Task, Result
# from nornir_utils.plugins.functions import print_result
# from nornir_nautobot.plugins.tasks.dispatcher import dispatcher

LOGGER = logging.getLogger(__name__)


def collect_info(task):

    mac_list = []
    cmd = "show mac address dynamic"

    output = task.run(task=netmiko_send_command, use_textfsm=True, command_string=cmd)

    mac_list.append(output.result)

    task.host["maclist"] = mac_list[0]

    for entry in mac_list[0]:

        # print(entry[0]['mac_address'])
        print(
            f"{task.host} {entry['mac_address']: ^20} {entry['vlan_id']: <6} {entry['ports']}"
        )


def main():

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

    # Run the Norn!
    result = nr.run(task=collect_info)


if __name__ == "__main__":
    main()
