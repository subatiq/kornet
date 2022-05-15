from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from chieftane.fleet.models import Machine
from chieftane.strategy.orders.models import Order


class SSHCommunicator(ABC):
    @asynccontextmanager  # type: ignore
    async def shared_session(self, machine: Machine) -> AsyncIterator[Any]:
        raise NotImplementedError

    @abstractmethod
    async def execute_in_session(self, orders: list[Order], machine: Machine) -> list[Order]:
        raise NotImplementedError
