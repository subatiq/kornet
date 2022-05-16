from kornet.strategy.orders.recon.enum import ReconCatalog
from kornet.strategy.orders.recon.orders import _GET_CPU, _GET_HOSTNAME, _GET_OS, _GET_RAM

RECON_CATALOG = {
    ReconCatalog.OS: _GET_OS,
    ReconCatalog.CPU: _GET_CPU,
    ReconCatalog.RAM: _GET_RAM,
    ReconCatalog.HOSTNAME: _GET_HOSTNAME,
}
