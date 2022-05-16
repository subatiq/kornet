from contextlib import asynccontextmanager
from typing import AsyncIterator

import paramiko
from loguru import logger

from kornet.fleet.models import Machine
from kornet.strategy.adapters.abstract import SSHCommunicator
from kornet.strategy.orders.models import Order, OrderOutcome


class ParamikoSSHCommunicator(SSHCommunicator):
    def _execute_command(self, session: paramiko.SSHClient, command: str) -> OrderOutcome:
        (_, stdout, stderr) = session.exec_command(command)

        stdout_lines = [line.strip() for line in stdout.readlines()]
        stderr_lines = [line.strip() for line in stderr.readlines()]
        exit_code = stdout.channel.recv_exit_status()

        return OrderOutcome(code=exit_code, outputs=stdout_lines, errors="\n".join(stderr_lines))

    @asynccontextmanager
    async def shared_session(self, machine: Machine) -> AsyncIterator[paramiko.SSHClient]:
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

    async def execute_in_session(self, session: paramiko.SSHClient, order: Order) -> Order:
        order.outcome = self._execute_command(session, order.command)
        return order
