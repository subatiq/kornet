from __future__ import annotations

from typing import TYPE_CHECKING

from kornet.strategy.machines.models import OS, RAM, Processor

if TYPE_CHECKING:
    from kornet.strategy.orders.models import OrderOutcome


def os_parser(outcome: OrderOutcome) -> OS:
    known_facts = {"name": "", "version": ""}

    for line in outcome.outputs:
        if line.startswith("NAME="):
            known_facts["name"] = line.split("=")[1].replace('"', "")
        elif line.startswith("VERSION="):
            known_facts["version"] = line.split("=")[1].replace('"', "")

    return OS(**known_facts)


def cpu_parser(outcome: OrderOutcome) -> Processor:
    known_facts = {"model": "", "cores": 0, "arch": ""}

    for line in outcome.outputs:
        if line.startswith("model name"):
            known_facts["model"] = line.split(":")[1].strip()

    known_facts["cores"] = int(outcome.outputs[-2].strip())
    known_facts["arch"] = outcome.outputs[-1].strip()

    return Processor(**known_facts)


def ram_parser(outcome: OrderOutcome) -> RAM:
    known_facts = {"total": 0, "available": 0}
    for line in outcome.outputs:
        if line.startswith("Mem"):
            known_facts["total"] = int(line.split()[1])
            known_facts["available"] = int(line.split()[3])
            break

    return RAM(**known_facts)
