#!/usr/bin/env python3
# collect_info.py

from nr_init import nr_init
from nornir_netmiko.tasks import netmiko_send_command


# reusable function for collecting command output and storing it
def collect_info(task, info, cmd):
    th_var = info
    info = []
    output = task.run(task=netmiko_send_command, use_textfsm=True, command_string=cmd)
    info.append(output.result)
    task.host[th_var] = info[0]


# function to parse arp table output
def arp_info(task):
    for entry in task.host["arp_list"]:
        # print(entry)
        print(f"{task.host} {entry['mac_address']: ^20} {entry['ip_address']} ")


# function to parse mac table output
def mac_info(task):
    for entry in task.host["mac_list"]:
        print(
            f"{task.host} {entry['mac_address']: ^20} {entry['vlan_id']: <6} {entry['ports']}"
        )


# It's Norn time!
def main():
    # Init the Norn!
    nr = nr_init()
    # Run the Norn! (ARP)
    result = nr.run(task=collect_info, info="arp_list", cmd="show ip arp")
    result = nr.run(task=arp_info)
    print()
    # Run the Norn! (MAC)
    result = nr.run(task=collect_info, info="mac_list", cmd="show mac address dynamic")
    result = nr.run(task=mac_info)


if __name__ == "__main__":
    main()
