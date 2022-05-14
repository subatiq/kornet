from typing import Any, Tuple

from chieftane.fleet.models import Fleet, Machine
from chieftane.fleet.raw.hosts_parser import parse_fleet_object
from chieftane.strategy.adapters.paramiko_ssh_comm import ParamikoSSHCommunicator
from chieftane.strategy.models import Strategy, StrategyOutcome
from chieftane.strategy.raw.strategy_parser import parse_strategy_object
from chieftane.strategy.services import execute_strategy_on_fleet


def strategize(*, recon: list[dict[str, Any]] = [], orders: list[dict[str, Any]] = []) -> Strategy:
    return parse_strategy_object({"recon": recon, "orders": orders})


def prepare_fleet(fleet_raw: dict[str, Any], group: str) -> Fleet:
    return parse_fleet_object(fleet_raw, group)


def execute_strategy(strategy: Strategy, fleet: Fleet) -> dict[Machine, StrategyOutcome]:
    return execute_strategy_on_fleet(ParamikoSSHCommunicator(), strategy, fleet)
