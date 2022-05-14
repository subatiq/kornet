from chieftane.strategy.orders.recon.orders import _GET_CPU, _GET_OS, _GET_RAM


RECON_CATALOG = {
    'os': _GET_OS,
    'cpu': _GET_CPU,
    'ram': _GET_RAM,
}
