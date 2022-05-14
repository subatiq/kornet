from __future__ import annotations

from typing import Union

from chieftane.shared.models import Model
from chieftane.strategy.models import Strategy
from chieftane.strategy.orders.models import Order
from chieftane.strategy.orders.recon.catalog import RECON_CATALOG
from chieftane.strategy.orders.recon.models import Recon, ReconAlias


class RawStrategy(Model):
    recon: list[Union[ReconAlias, Recon]]
    orders: list[Order] = list()

    def to_strategy(self) -> Strategy:
        parsed_recon = []
        parsed_orders = []
        for order in self.orders + self.recon:  # type: ignore
            if isinstance(order, ReconAlias):
                parsed_recon.append(RECON_CATALOG[order.__root__])
            elif isinstance(order, Recon):
                parsed_recon.append(order)
            else:
                parsed_orders.append(order)

        return Strategy(orders=parsed_orders, recon=parsed_recon)
