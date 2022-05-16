from __future__ import annotations

from kornet.fleet.models import Machine
from kornet.shared.models import Model
from kornet.strategy.machines.models import MachineFacts
from kornet.strategy.orders.models import Order
from kornet.strategy.orders.recon.models import Recon


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
