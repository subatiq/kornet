from __future__ import annotations

from typing import Optional

from kornet.shared.models import Model


class MachineInfo(Model):
    pass


class OS(MachineInfo):
    name: str
    version: str


class Processor(MachineInfo):
    model: str
    cores: int
    arch: str


class Memory(MachineInfo):
    total: int
    available: int


class RAM(Memory):
    pass


class Disk(Memory):
    pass


class MachineFacts(Model):
    cpu: Optional[Processor] = None
    ram: Optional[RAM] = None
    os: Optional[OS] = None

    def append(self, info: MachineInfo) -> None:
        if isinstance(info, Processor):
            self.cpu = info
        elif isinstance(info, RAM):
            self.ram = info
        elif isinstance(info, OS):
            self.os = info

    def update(self, other: MachineFacts) -> None:
        self.__dict__.update(other.__dict__)
