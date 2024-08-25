#!/usr/bin/env python3
# arpquery.py

from nr_init import nr_init
from nornir_netmiko.tasks import netmiko_send_command


def collect_info(task):
    arp_list = []
    cmd = "show ip arp"
    output = task.run(task=netmiko_send_command, use_textfsm=True, command_string=cmd)
    arp_list.append(output.result)
    task.host["arplist"] = arp_list[0]
    for entry in arp_list[0]:
        print(f"{task.host} {entry['mac_address']: ^20} {entry['ip_address']} ")


def main():
    # Init the Norn!
    nr = nr_init()
    # Run the Norn!
    result = nr.run(task=collect_info)


if __name__ == "__main__":
    main()
