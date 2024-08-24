#!/usr/bin/env python3
"""Testing file."""

# pylint: disable=duplicate-code
import logging
import os
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir_nautobot.plugins.tasks.dispatcher import dispatcher


LOGGER = logging.getLogger(__name__)


# Disabling pylint for example
from nornir_utils.plugins.functions import print_result  # pylint: disable=import-error


def hello_world(task: Task) -> Result:
    """Example to show work inside of a task.

    Args:
        task (Task): Nornir Task

    Returns:
        Result: Nornir result
    """
    return Result(
        host=task.host, result=f"{task.host.name} says hello world, from Nautobot!!"
    )


def main():
    """Nornir testing."""
    my_nornir = InitNornir(
        inventory={
            "plugin": "NautobotInventory",
            "options": {
                "nautobot_url": os.getenv("NAUTOBOT_URL"),
                "nautobot_token": os.getenv("NAUTBOT_TOKEN"),
                "filter_parameters": {"location": "Home"},
                "ssl_verify": False,
            },
        },
    )

    my_nornir.inventory.defaults.username = os.getenv("NORNIR_USERNAME")
    my_nornir.inventory.defaults.password = os.getenv("NORNIR_PASSWORD")

    print(f"Hosts found: {len(my_nornir.inventory.hosts)}")
    # Print out the keys for the inventory
    print(my_nornir.inventory.hosts.keys())

    result = my_nornir.run(task=hello_world)
    print_result(result)

    for nr_host, nr_obj in my_nornir.inventory.hosts.items():
        network_driver = my_nornir.inventory.hosts[nr_host].platform
        result = my_nornir.run(
            task=dispatcher,
            logger=LOGGER,
            method="get_config",
            obj=nr_host,
            framework="netmiko",
            backup_file="./ios.cfg",
            remove_lines=None,
            substitute_lines=None,
        )
        print_result(result)


if __name__ == "__main__":
    main()
