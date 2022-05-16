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
    hostname: Optional[str] = None
    cpu: Optional[Processor] = None
    ram: Optional[RAM] = None
    os: Optional[OS] = None

    def update(self, other: MachineFacts) -> None:
        updated = self.dict()
        updated.update(other.dict(exclude_unset=True, exclude_none=True))
        self.__dict__.update(MachineFacts(**updated).__dict__)
