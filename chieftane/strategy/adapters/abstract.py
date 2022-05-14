from abc import ABC, abstractmethod

from chieftane.fleet.models import Machine
from chieftane.strategy.orders.models import Order


class SSHCommunicator(ABC):
    @abstractmethod
    def execute_order(self, order: Order, machine: Machine) -> Order:
        raise NotImplementedError

    @abstractmethod
    def batch_execute_orders(self, orders: list[Order], machine: Machine) -> list[Order]:
        raise NotImplementedError
