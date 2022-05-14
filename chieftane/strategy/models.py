from __future__ import annotations

from chieftane.shared.models import Model
from chieftane.strategy.machines.models import MachineInfo
from chieftane.strategy.orders.models import Order
from chieftane.strategy.orders.recon.models import Recon


class StrategyOutcome(Model):
    recon: list[MachineInfo]
    success: list[Order]
    error: list[Order]


class Strategy(Model):
    recon: list[Recon] = list()
    orders: list[Order] = list()

    @property
    def outcome(self) -> StrategyOutcome:
        success = []
        error = []
        recon = []
        for order in self.orders:
            if not order.outcome:
                continue
            if order.failed:
                error.append(order)
            elif isinstance(order, Recon):
                recon.append(order.intel)
            else:
                success.append(order)

        return StrategyOutcome(success=success, error=error, recon=recon)
