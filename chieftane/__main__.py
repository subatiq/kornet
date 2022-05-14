import typer

from pathlib import Path
from chieftane.fleet.raw.hosts_parser import parse_fleet_file
from chieftane.strategy.adapters.paramiko_ssh_comm import ParamikoSSHCommunicator
from chieftane.strategy.services import execute_strategy
from chieftane.strategy.raw.strategy_parser import parse_strategy_file


def main(strategy_filepath: Path, fleet_filepath: Path, group: str):
    inv = parse_fleet_file(fleet_filepath, group)
    execute_strategy(ParamikoSSHCommunicator(), parse_strategy_file(strategy_filepath), inv)


if __name__ == "__main__":
    typer.run(main)
