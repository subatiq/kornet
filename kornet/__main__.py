from pathlib import Path

import typer
import yaml

from kornet import execute_strategy, prepare_fleet, strategize


def main(strategy_filepath: Path, fleet_filepath: Path, group: str):
    fleet = prepare_fleet(yaml.safe_load(fleet_filepath.read_text()), group)
    strategy = strategize(**yaml.safe_load(strategy_filepath.read_text()))
    execute_strategy(strategy, fleet)


if __name__ == "__main__":
    typer.run(main)
