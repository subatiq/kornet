import getpass
from ipaddress import IPv4Address
from pathlib import Path

import typer
import yaml
from pydantic import SecretStr

from kornet import execute_strategy, prepare_fleet
from kornet import recon as exec_recon
from kornet import strategize
from kornet.fleet.models import Machine
from kornet.shared.models import SSHProps
from kornet.strategy.orders.recon.enum import ReconCatalog

app = typer.Typer()


@app.command()
def run(strategy_filepath: Path, fleet_filepath: Path, group: str):
    fleet = prepare_fleet(yaml.safe_load(fleet_filepath.read_text()), group)
    strategy = strategize(**yaml.safe_load(strategy_filepath.read_text()))
    execute_strategy(strategy, fleet)


@app.command()
def recon(
    recon: ReconCatalog,
    host: str = typer.Argument(..., help="<username>@<hostname>"),
    port: int = 22,
):
    machine = Machine(
        ip=IPv4Address(host.split("@")[-1]),
        ssh=SSHProps(
            username=host.split("@")[0],
            password=SecretStr(getpass.getpass("Password: ")),
            port=port,
        ),
    )

    facts = exec_recon(recon, machine).yaml(exclude_none=True)
    print()  # noqa: T001
    print("Results:")  # noqa: T001
    print(facts)  # noqa: T001


app()
