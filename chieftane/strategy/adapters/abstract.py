from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from chieftane.fleet.models import Machine
from chieftane.strategy.orders.models import Order


class SSHCommunicator(ABC):
    @asynccontextmanager
    async def shared_session(self, machine: Machine):
        raise NotImplementedError

    @abstractmethod
    async def execute_in_session(self, orders: list[Order], machine: Machine) -> list[Order]:
        raise NotImplementedError
