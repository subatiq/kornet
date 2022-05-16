from typing import Any

from kornet.fleet.models import Fleet, Machine
from kornet.fleet.raw.hosts_parser import parse_fleet_object
from kornet.strategy.adapters.asyncssh_comm import AsyncSSHCommunicator
from kornet.strategy.models import Strategy, StrategyOutcome
from kornet.strategy.raw.strategy_parser import parse_strategy_object
from kornet.strategy.services import execute_strategy_on_fleet


def strategize(*, recon: list[dict[str, Any]] = [], orders: list[dict[str, Any]] = []) -> Strategy:
    return parse_strategy_object({"recon": recon, "orders": orders})


def prepare_fleet(fleet_raw: dict[str, Any], group: str) -> Fleet:
    return parse_fleet_object(fleet_raw, group)


def execute_strategy(strategy: Strategy, fleet: Fleet) -> dict[Machine, StrategyOutcome]:
    return execute_strategy_on_fleet(AsyncSSHCommunicator(), strategy, fleet)
