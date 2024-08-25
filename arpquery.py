#!/usr/bin/env python3
# arpquery.py

import logging
import os
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir_nautobot.plugins.tasks.dispatcher import dispatcher
from nornir_netmiko.tasks import netmiko_send_command

LOGGER = logging.getLogger(__name__)

def main():
    """Nornir testing."""
    my_nornir = InitNornir(
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

    my_nornir.inventory.defaults.username = os.getenv("NORNIR_USERNAME")
    my_nornir.inventory.defaults.password = os.getenv("NORNIR_PASSWORD")

    print(f"Hosts found: {len(my_nornir.inventory.hosts)}")
    # Print out the keys for the inventory
    print(my_nornir.inventory.hosts.keys())

    cmd = "sh ip arp detail vrf all"
    for nr_host, nr_obj in my_nornir.inventory.hosts.items():
        network_driver = my_nornir.inventory.hosts[nr_host].platform
        output = my_nornir.run(task=netmiko_send_command, use_textfsm=True, command_string=cmd)        
    
    print_result(output)


if __name__ == "__main__":
    main()
