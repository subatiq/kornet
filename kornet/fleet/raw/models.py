from ipaddress import IPv4Address
from typing import Any

from kornet.shared.models import Model, SSHProps


class Host(Model):
    ip: IPv4Address
    ssh: SSHProps = SSHProps()
    groups: set[str]

    def __hash__(self) -> int:
        return hash(self.ip)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Host):
            return False
        return self.ip == other.ip


class Group(Model):
    ssh: SSHProps


class Hosts(Model):
    hosts: set[Host]
    groups: dict[str, Group]
