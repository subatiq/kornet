from pathlib import Path
from typing import Any

import yaml

from kornet.fleet.models import Fleet, Machine
from kornet.fleet.raw.models import Hosts
from kornet.shared.models import SSHProps


def merge_ssh_configs(host_config: dict, group_config: dict) -> SSHProps:

    return SSHProps(**(group_config | host_config))


def parse_fleet_object(fleet: dict[str, Any], group: str) -> Fleet:
    hosts = fleet.get("hosts", [])
    groups = fleet.get("groups", {})
    for host in hosts:
        if group in host.get("groups", []):
            host["ssh"] = merge_ssh_configs(host.get("ssh", {}), groups[group].get("ssh", {}))

    hosts = Hosts(**fleet)
    hosts_in_group = [host for host in hosts.hosts if group in host.groups]

    return Fleet(machines={Machine(ip=host.ip, ssh=host.ssh) for host in hosts_in_group})


def parse_fleet_file(file_path: Path, group: str) -> Fleet:
    config_dict = yaml.safe_load(file_path.read_text())
    return parse_fleet_object(config_dict, group)
