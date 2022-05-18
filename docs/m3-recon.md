# Recon

Recon is a type of an order that returns either plain `str` or `MachineFacts` object. 

!!! warning
    As everything in this library, these approaches were only tested on Ubuntu and Raspbian. Do not rely on it too much. Nevertheless, recon is read-only and expected to be non-destructive. 

## Machine Facts

```python
class MachineFacts(Model):
    hostname: Optional[str] = None
    cpu: Optional[Processor] = None
    ram: Optional[RAM] = None
    os: Optional[OS] = None
```

### Hostname

A plain string value returned from a `hostname` command.

### OS

```python
class OS(MachineInfo):
    name: str
    version: str
```

Parses info in output of 

```bash
cat /etc/os-release
```

### CPU

CPU structures information about CPU of the target machine:

```python
class Processor(MachineInfo):
    model: str
    cores: int
    arch: str
```

It gets it by executing and parsing three commands:

```bash
cat /proc/cpuinfo && getconf _NPROCESSORS_ONLN && arch
```

### Memory

Memory is a parent for all parameters following a memory format: having total bytes and available bytes

```python
class Memory(MachineInfo):
    total: int
    available: int

```

#### RAM

```python
class RAM(Memory):
    pass
```

Gets ram by executing `free` command.

#### Disk

```python
class Disk(Memory):
    pass

```

Not implemented
