from __future__ import annotations

from kornet.strategy.orders.recon.handlers import cpu_parser, os_parser, ram_parser
from kornet.strategy.orders.recon.models import Recon

_GET_OS = Recon(
    name="Get OS info",
    command="cat /etc/os-release",
    handler=os_parser,
)

_GET_CPU = Recon(
    name="Get CPU info",
    command="cat /proc/cpuinfo && getconf _NPROCESSORS_ONLN && arch",
    handler=cpu_parser,
)

_GET_RAM = Recon(name="Get RAM info", command="free", handler=ram_parser)
