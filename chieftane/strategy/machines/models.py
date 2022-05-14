from typing import Optional

from chieftane.shared.models import Model


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
 