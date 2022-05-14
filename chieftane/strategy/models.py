from __future__ import annotations
from chieftane.shared.models import Model

from chieftane.strategy.orders.models import Order
from chieftane.strategy.raw.models import RawStrategy


class StrategyOutcome(Model):
    success: list[Order]
    error: list[Order]


class Strategy(Model):
    orders: list[Order] = list() 

    @staticmethod
    def from_raw(raw: RawStrategy) -> Strategy:
        return Strategy(orders=raw.parsed_orders(raw.__root__))

    @property
    def outcome(self) -> StrategyOutcome:
        success = []
        error = []
        for order in self.orders:
            if not order.outcome:
                continue
            if order.failed :
                error.append(order)
            else:
                success.append(order)

        return StrategyOutcome(success=success, error=error)
