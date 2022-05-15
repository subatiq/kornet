from contextlib import contextmanager
from typing import Iterator

import paramiko
from loguru import logger

from chieftane.fleet.models import Machine
from chieftane.strategy.adapters.abstract import SSHCommunicator
from chieftane.strategy.orders.models import Order, OrderOutcome


class ParamikoSSHCommunicator(SSHCommunicator):
    def _execute_command(self, session: paramiko.SSHClient, command: str) -> OrderOutcome:
        (_, stdout, stderr) = session.exec_command(command)

        stdout_lines = [line.strip() for line in stdout.readlines()]
        stderr_lines = [line.strip() for line in stderr.readlines()]
        exit_code = stdout.channel.recv_exit_status()

        return OrderOutcome(code=exit_code, outputs=stdout_lines, errors="\n".join(stderr_lines))

    @contextmanager
    def shared_session(self, machine: Machine) -> Iterator[paramiko.SSHClient]:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            session.connect(
                str(machine.ip),
                port=machine.ssh.port,
                username=machine.ssh.username,
                password=machine.ssh.password.get_secret_value(),
            )
        except OSError as err:
            logger.error(f"Failed to connect to {machine.ip}: {err}")

        yield session
        session.close()

    # def execute_order(self, order: Order, machine: Machine) -> Order:
    #     with self.shared_session(machine) as session:
    #         return self.execute_in_session(session, order)

    def execute_in_session(self, session: paramiko.SSHClient, order: Order) -> Order:
        order.outcome = self._execute_command(session, order.command)
        return order

    async def execute_in_session_async(self, session: paramiko.SSHClient, order: Order) -> Order:
        return self.execute_in_session(session, order)
