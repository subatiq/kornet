from contextlib import contextmanager
from typing import Iterator

import paramiko
from pydantic import SecretStr

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
    def _create_session(
        self, host: str, port: int, user: str, password: SecretStr
    ) -> Iterator[paramiko.SSHClient]:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(host, port, user, password.get_secret_value())

        yield session
        session.close()

    def execute_order(self, order: Order, machine: Machine) -> Order:
        with self._create_session(
            str(machine.ip), machine.ssh.port, machine.ssh.username, machine.ssh.password
        ) as session:
            order.outcome = self._execute_command(session, order.command)
            return order

    def batch_execute_orders(self, orders: list[Order], machine: Machine) -> list[Order]:
        with self._create_session(
            str(machine.ip), machine.ssh.port, machine.ssh.username, machine.ssh.password
        ) as session:
            for order in orders:
                order.outcome = self._execute_command(session, order.command)

            return orders
