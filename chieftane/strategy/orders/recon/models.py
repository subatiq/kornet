from ipaddress import IPv4Address
from typing import Callable, Optional

from chieftane.shared.models import Model
from chieftane.strategy.machines.models import MachineFacts, MachineInfo
from chieftane.strategy.orders.models import Order, OrderOutcome
from chieftane.strategy.orders.recon.enum import ReconCatalog


class ReconAlias(Model):
    __root__: ReconCatalog


class FleetInfo(Model):
    machines: dict[IPv4Address, MachineFacts]


class Recon(Order):
    handler: Callable[[OrderOutcome], MachineInfo]

    @property
    def intel(self) -> Optional[MachineInfo]:
        if not self.outcome or self.failed:
            return None

        return self.handler(self.outcome)
