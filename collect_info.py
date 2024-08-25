#!/usr/bin/env python3
# collect_info.py

from nornir_netmiko.tasks import netmiko_send_command

from nr_init import nr_init


# function for collecting parsed command output and storing it
def collect_info(task, th_var, cmd):
    # Nornir connects to devices using Netmiko here
    output = task.run(task=netmiko_send_command, use_textfsm=True, command_string=cmd)
    # add parsed command output to task.host variable
    task.host[th_var] = output.result


# function to parse arp table output
def arp_info(task):
    for entry in task.host["arp_list"]:
        print(f"{task.host} {entry['mac_address']: ^20} {entry['ip_address']} ")


# function to parse mac table output
def mac_info(task):
    for entry in task.host["mac_list"]:
        print(
            f"{task.host} {entry['mac_address']: ^20} {entry['vlan_id']: <6} {entry['ports']}"
        )


# It's Norn time!
def main():
    # set Nautobot Location filter (or leave blank for all)
    location_filter = ["Lab_A"]
    # Init the Norn!
    nr = nr_init(location_filter)
    # Run the Norn! (get ARP tables)
    result = nr.run(task=collect_info, th_var="arp_list", cmd="show ip arp")
    # Run the Norn! (process ARP tables)
    result = nr.run(task=arp_info)
    print()
    # Run the Norn! (get MAC tables)
    result = nr.run(
        task=collect_info, th_var="mac_list", cmd="show mac address dynamic"
    )
    # Run the Norn! (process MAC tables)
    result = nr.run(task=mac_info)


if __name__ == "__main__":
    main()
