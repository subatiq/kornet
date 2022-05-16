from __future__ import annotations

from enum import Enum
from ipaddress import IPv4Address
from typing import Any

from kornet.shared.models import Model, SSHProps
from kornet.strategy.machines.models import MachineFacts


class MachineState(str, Enum):
    OK = "OK"
    UNREACHABLE = "UNREACHABLE"
    FAILED = "FAILED"


class Machine(Model):
    ip: IPv4Address
    ssh: SSHProps
    facts: MachineFacts = MachineFacts()
    state: MachineState = MachineState.UNREACHABLE

    def __hash__(self) -> int:
        return hash(self.ssh.username + str(self.ip))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Machine):
            return False
        return hash(self) == hash(other)


class Fleet(Model):
    machines: set[Machine]
