from __future__ import annotations
from typing import Union
from chieftane.shared.models import Model
from chieftane.strategy.orders.models import Order
from chieftane.strategy.orders.recon.models import ReconAlias
from chieftane.strategy.orders.recon.catalog import RECON_CATALOG


class RawStrategy(Model):
    __root__: list[Union[Order, ReconAlias]] = list()

    def parsed_orders(self, orders: list[Union[Order, ReconAlias]]) -> list[Order]:
        parsed_orders = []
        for order in orders:
            if isinstance(order, ReconAlias):
                parsed_orders.append(RECON_CATALOG[order.recon.lower()])
            else:
                parsed_orders.append(order)

        return parsed_orders
