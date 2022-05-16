from typing import Optional

from kornet.shared.models import Model


class OrderOutcome(Model):
    code: int
    outputs: list[str]
    errors: str


class Order(Model):
    name: Optional[str] = None
    command: str
    silent: bool = False
    outcome: Optional[OrderOutcome] = None

    @property
    def failed(self) -> bool:
        return self.outcome is not None and len(self.outcome.errors) > 0
