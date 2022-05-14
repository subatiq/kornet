from __future__ import annotations

from ipaddress import IPv4Address
from typing import Any

from chieftane.shared.models import Model, SSHProps
from chieftane.strategy.machines.models import MachineFacts


class Machine(Model):
    ip: IPv4Address
    ssh: SSHProps
    facts: MachineFacts = MachineFacts()

    def __hash__(self) -> int:
        return hash(self.ip)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Machine):
            return False
        return self.ip == other.ip


class Fleet(Model):
    machines: set[Machine]
