"""
Basic use cases implemented:
- gather intel on host
- execute strategy on host
- execute strategy on fleet
"""

from loguru import logger

from chieftane.fleet.models import Fleet, Machine
from chieftane.strategy.adapters.abstract import SSHCommunicator
from chieftane.strategy.machines.models import MachineFacts
from chieftane.strategy.models import Strategy, StrategyOutcome
from chieftane.strategy.orders.models import Order, OrderOutcome
from chieftane.strategy.orders.recon.models import Recon


def get_host_facts(comm: SSHCommunicator, orders: list[Recon], host: Machine) -> MachineFacts:
    facts = MachineFacts()
    for order in orders:
        execute_order(comm, order, host)
        if not order.intel:
            continue
        facts.append(order.intel)

    return facts


def handle_failed_order(order: Order, host: Machine):
    logger.error(f'Failed to execute order "{order.name}" on {host.ip}')
    if order.outcome:
        logger.error(f"{order.outcome.errors}")


def handle_successful_order(order: Order, host: Machine):
    if isinstance(order, Recon) and order.intel:
        logger.info(f"Got intel from {order.name} on {host.ip}:\n{order.intel.yaml()}")
    elif order.outcome:
        logger.info(
            'Order "{}" on {} finished with \n\tExit code: {}\n\tOutput:\n{}',
            order.name,
            host.ip,
            order.outcome.code,
            order.outcome.yaml(),
        )


def execute_order(comm: SSHCommunicator, order: Order, host: Machine, hide_output=False):
    order.silent = hide_output or order.silent

    logger.info(f'Executing order "{order.name}" on {host.ip}')
    try:
        order = comm.execute_order(order, host)
    except Exception as exc:
        logger.error(f'Failed to execute order "{order.name}" on {host.ip}. Error: {exc}')
        order.outcome = OrderOutcome(code=-1, outputs=[], errors=str(exc))

    if order.failed or not order.outcome:
        handle_failed_order(order, host)
    elif not order.silent:
        logger.info(f'Successfully executed order "{order.name}" on {host.ip}')
        handle_successful_order(order, host)

    return order


def execute_strategy_on_host(
    comm: SSHCommunicator, strategy: Strategy, host: Machine, recon: bool = True
) -> StrategyOutcome:
    """Execute strategy on host"""
    outcome = StrategyOutcome()
    if recon:
        outcome.facts.update(get_host_facts(comm, strategy.recon, host))

    for order in strategy.orders:
        if isinstance(order, Recon) and not recon:
            continue

        execute_order(comm, order, host)
        outcome.orders.append(order)

        if order.failed:
            break

    logger.info(
        "Finished executing strategy on {}@{}:{}. Outcomes:\nSuccess: {}\nError: {}\n",
        host.ssh.username,
        host.ip,
        host.ssh.port,
        len(strategy.successful_orders),
        len(strategy.failed_orders),
    )

    return outcome


def execute_strategy_on_fleet(
    comm: SSHCommunicator, strategy: Strategy, fleet: Fleet, recon: bool = True
) -> dict[Machine, StrategyOutcome]:
    """Execute strategy on fleet"""
    for host in fleet.machines:
        strategy.outcome[host] = execute_strategy_on_host(comm, strategy, host, recon)

    return strategy.outcome
