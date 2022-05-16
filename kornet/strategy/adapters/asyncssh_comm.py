from contextlib import asynccontextmanager

from asyncssh.client import SSHClient
from asyncssh.connection import SSHClientConnection, create_connection
from loguru import logger

from kornet.fleet.models import Machine, MachineState
from kornet.strategy.adapters.abstract import SSHCommunicator
from kornet.strategy.orders.models import Order, OrderOutcome


class AsyncSSHCommunicator(SSHCommunicator):
    async def _execute_command(self, session: SSHClientConnection, command: str) -> OrderOutcome:
        result = await session.run(command, check=True)
        stdout_lines = result.stdout or ""
        stderr_lines = result.stderr or ""
        exit_code = result.exit_status or 0

        if isinstance(stdout_lines, bytes):
            stdout_lines = stdout_lines.decode()
        if isinstance(stderr_lines, bytes):
            stderr_lines = stderr_lines.decode()

        return OrderOutcome(
            code=exit_code,
            outputs=[line for line in stdout_lines.split("\n") if line],
            errors=stderr_lines,
        )

    async def execute_in_session(self, session: SSHClientConnection, order: Order) -> Order:
        order.outcome = await self._execute_command(session, order.command)
        return order

    @asynccontextmanager
    async def shared_session(self, machine: Machine):
        try:
            conn, _ = await create_connection(
                SSHClient,
                str(machine.ip),
                port=machine.ssh.port,
                username=machine.ssh.username,
                password=machine.ssh.password.get_secret_value(),
                known_hosts=None,
            )
            machine.state = MachineState.OK
            yield conn
            conn.close()

        except Exception as exc:
            machine.state = MachineState.UNREACHABLE
            logger.error(f"Failed to connect to {machine.ip}. Error: {exc}")
            yield None
