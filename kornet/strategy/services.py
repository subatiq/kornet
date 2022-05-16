"""
Basic use cases implemented:
- gather intel on host
- execute strategy on host
- execute strategy on fleet
"""

import asyncio
from copy import deepcopy

from loguru import logger

from kornet.fleet.models import Fleet, Machine, MachineState
from kornet.strategy.adapters.abstract import SSHCommunicator
from kornet.strategy.machines.models import MachineFacts
from kornet.strategy.models import Strategy, StrategyOutcome
from kornet.strategy.orders.models import Order, OrderOutcome
from kornet.strategy.orders.recon.models import Recon


async def get_host_facts(comm, orders: list[Recon], host: Machine) -> MachineFacts:
    facts = MachineFacts()
    async with comm.shared_session(host) as session:
        if not session:
            return facts
        for order in orders:
            await execute_order(comm, session, order, host, hide_output=True)
            if order.failed:
                break
            if not order.intel:
                continue
            facts.append(order.intel)

    return facts


def handle_failed_order(order: Order, host: Machine):
    logger.error(f'Failed to execute order "{order.name}" on {host.ip}')
    if order.outcome:
        logger.error(f"{order.outcome.errors}")

    host.state = MachineState.FAILED


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
    host.state = MachineState.OK


async def execute_order(comm, session, order: Order, host: Machine, hide_output=False):
    order.silent = hide_output or order.silent

    logger.info(f'Executing order "{order.name}" on {host.ip}')
    try:
        order = await comm.execute_in_session(session, order)
    except Exception as exc:
        logger.error(f'Failed to execute order "{order.name}" on {host.ip}. Error: {exc}')
        order.outcome = OrderOutcome(code=-1, outputs=[], errors=str(exc))

    if order.failed or not order.outcome:
        handle_failed_order(order, host)
    elif not order.silent:
        logger.info(f'Successfully executed order "{order.name}" on {host.ip}')
        handle_successful_order(order, host)

    return order


async def execute_strategy_on_host(
    comm: SSHCommunicator, strategy: Strategy, host: Machine, recon: bool = True
) -> StrategyOutcome:
    """Execute strategy on host"""
    outcome = StrategyOutcome()
    async with comm.shared_session(host) as session:
        if not session:
            return deepcopy(outcome)
        if recon:
            outcome.facts.update(await get_host_facts(comm, strategy.recon, host))

        for order in strategy.orders:
            if isinstance(order, Recon) and not recon:
                continue

            await execute_order(comm, session, order, host)
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

    return deepcopy(outcome)


async def async_execute_strategy_on_fleet(
    comm: SSHCommunicator, strategy: Strategy, fleet: Fleet, recon: bool = True
) -> dict[Machine, StrategyOutcome]:
    """Execute strategy on fleet"""
    tasks = (execute_strategy_on_host(comm, strategy, host, recon) for host in fleet.machines)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for host, outcome in zip(fleet.machines, results):
        strategy.outcome[host] = outcome

    return strategy.outcome


def execute_strategy_on_fleet(
    comm: SSHCommunicator, strategy: Strategy, fleet: Fleet, recon: bool = True
) -> dict[Machine, StrategyOutcome]:
    """Execute strategy on fleet"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(async_execute_strategy_on_fleet(comm, strategy, fleet, recon))
    return results
