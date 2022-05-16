from enum import Enum


class ReconCatalog(str, Enum):
    OS = "OS"
    CPU = "CPU"
    RAM = "RAM"
    HOSTNAME = "HOSTNAME"
