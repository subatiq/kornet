from ipaddress import IPv4Address
from chieftane.fleet.models import Fleet, Machine
from chieftane.strategy.adapters.abstract import SSHCommunicator
from chieftane.strategy.machines.models import MachineFacts
from chieftane.strategy.models import Strategy
from loguru import logger
from chieftane.strategy.orders.models import Order, OrderOutcome

from chieftane.strategy.orders.recon.catalog import RECON_CATALOG
from chieftane.strategy.orders.recon.models import Recon


def recon_fleet(comm: SSHCommunicator, fleet: Fleet) -> dict[IPv4Address, MachineFacts]:
    facts = {}
    for host in fleet.machines:
        machine_facts = MachineFacts()
        for key, recon in RECON_CATALOG.items():
            execute_order(comm, recon, host, hide_output=True)
            
            machine_facts.__setattr__(key, recon.intel)
    
        facts[host.ip] = machine_facts
        logger.info(f'Gathered info on {host.ip}:\n\t{machine_facts}')
    return facts

    
def gather_intel(comm: SSHCommunicator, order: Recon, host: Machine):
    execute_order(comm, order, host)
    return order.intel


def execute_order(comm: SSHCommunicator, order: Order, host: Machine, hide_output=False):
    logger.info(f'Executing order "{order.name}" on {host.ip}')
    try:
        order = comm.execute_order(order, host)
    except Exception as exc:
        logger.error(f'Failed to execute order "{order.name}" on {host.ip}. Error: {exc}')
        order.outcome = OrderOutcome(code=-1, outputs=[], errors=str(exc))

    if order.failed or not order.outcome:
        logger.error(f'Failed to execute order "{order.name}" on {host.ip}. ')
        if order.outcome:
            logger.error(f'{order.outcome.errors}')
    else:
        if hide_output or order.silent:
            return
        if isinstance(order, Recon) and order.intel:
            logger.info(
                f'Got intel from {order.name} on {host.ip}:\n{order.intel.yaml()}'
            )
        elif order.outcome.outputs:
            logger.info(
                f'Order "{order.name}" on {host.ip} finished with \n\tExit code: {order.outcome.code}\n\tOutput:\n{order.outcome.yaml()}'
            )


def execute_strategy(comm: SSHCommunicator, strategy: Strategy, inventory: Fleet):
    for host in inventory.machines:
        for order in strategy.orders:
            execute_order(comm, order, host)
            if order.failed:
                break

        logger.info(
            f'Finished executing strategy on {host.ssh.username}@{host.ip}:{host.ssh.port}. Outcomes:\nSuccess: {len(strategy.outcome.success)}\nError: {len(strategy.outcome.error)}\n' + '-' * 80
        )
