
from typing import Callable, Optional

from chieftane.shared.models import Model
from chieftane.strategy.machines.models import MachineInfo
from chieftane.strategy.orders.models import Order, OrderOutcome


class ReconAlias(Model):
    recon: str


class Recon(Order):
    handler: Callable[[OrderOutcome], MachineInfo]

    @property
    def intel(self) -> Optional[MachineInfo]:
        if not self.outcome or self.failed:
            return None

        return self.handler(self.outcome)
