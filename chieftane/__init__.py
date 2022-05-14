from typing import Any

from chieftane.fleet.models import Fleet
from chieftane.fleet.raw.hosts_parser import parse_fleet_object
from chieftane.strategy.adapters.paramiko_ssh_comm import ParamikoSSHCommunicator
from chieftane.strategy.models import Strategy, StrategyOutcome
from chieftane.strategy.raw.strategy_parser import parse_strategy_object
from chieftane.strategy.services import execute_strategy_on_fleet


def strategize(raw_strategy: list[dict[str, Any]]) -> Strategy:
    return parse_strategy_object(raw_strategy)


def prepare_fleet(fleet_raw: dict[str, Any], group: str) -> Fleet:
    return parse_fleet_object(fleet_raw, group)


def execute_strategy(strategy: Strategy, fleet: Fleet) -> StrategyOutcome:
    return execute_strategy_on_fleet(ParamikoSSHCommunicator(), strategy, fleet)
