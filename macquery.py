#!/usr/bin/env python3
# macquery.py

from nornir_netmiko.tasks import netmiko_send_command

from nr_init import nr_init


def collect_info(task):
    mac_list = []
    cmd = "show mac address dynamic"
    output = task.run(task=netmiko_send_command, use_textfsm=True, command_string=cmd)
    mac_list.append(output.result)
    task.host["maclist"] = mac_list[0]
    for entry in mac_list[0]:
        print(
            f"{task.host} {entry['mac_address']: ^20} {entry['vlan_id']: <6} {entry['ports']}"
        )


def main():
    # Init the Norn!
    nr = nr_init()
    # Run the Norn!
    result = nr.run(task=collect_info)


if __name__ == "__main__":
    main()
