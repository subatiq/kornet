from ipaddress import IPv4Address
from typing import Callable, Optional

from kornet.shared.models import Model
from kornet.strategy.machines.models import MachineFacts, MachineInfo
from kornet.strategy.orders.models import Order, OrderOutcome
from kornet.strategy.orders.recon.enum import ReconCatalog


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
