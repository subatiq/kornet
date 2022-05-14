from __future__ import annotations

from chieftane.fleet.models import Machine
from chieftane.shared.models import Model
from chieftane.strategy.machines.models import MachineFacts
from chieftane.strategy.orders.models import Order
from chieftane.strategy.orders.recon.models import Recon


class StrategyOutcome(Model):
    facts: MachineFacts = MachineFacts()
    orders: list[Order] = []


class Strategy(Model):
    recon: list[Recon] = list()
    orders: list[Order] = list()
    outcome: dict[Machine, StrategyOutcome] = dict()

    @property
    def successful_orders(self) -> list[Order]:
        return [
            order for order in [*self.orders, *self.recon] if order.outcome and not order.failed
        ]

    @property
    def failed_orders(self) -> list[Order]:
        return [order for order in [*self.orders, *self.recon] if order.failed]
