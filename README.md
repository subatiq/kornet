![](docs/logo/full_logo.svg)

<p align="center">
  <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/subatiq/kornet?style=for-the-badge">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/kornet?color=blue&style=for-the-badge">
  <img alt="GitHub" src="https://img.shields.io/github/license/subatiq/kornet?color=blue&style=for-the-badge">
  <img alt="Gitlab code coverage" src="https://img.shields.io/gitlab/coverage/subatiq/kornet/master?style=for-the-badge">
  <img alt="Code style" src="https://img.shields.io/badge/code%20style-black-black?style=for-the-badge">
</p>

---
A library for mass execution of ssh commands on remote machines fleet. 

More docs: https://subatiq.github.io/kornet/

## Installation

```bash
pip install kornet
```

## Usage examples

### Run multiple commands

```
kornet run <strategy_file.yml> <fleet_file.yml> <group>
```

**strategy file** - yaml strategy file described above

**fleet file** - yaml fleet file described above

**group** - group to run the strategy on

```bash
$ kornet run strategy.yml fleet.yml office

...
Lots of output with results
...
```

### Fast machine recon

```bash
$ kornet recon CPU user@192.168.0.2 --port 5022

Results:
cpu:
  arch: x86_64
  cores: 8
  model: Intel(R) Core(TM) i5-8265U CPU @ 1.60GHz
```

## Hosts file format

You need to specify hosts and their groups. Groups so far can store only simple SSH configurations (username, password and port). Each host can override these values by specifying certain fields.

```yaml
hosts:
- ip: 192.168.0.2
  groups: 
  - office
- ip: 192.168.0.3
  ssh:
    username: user  # overrides group value
  groups:
  - office

groups:
  office:
    ssh:
      username: root
      password: toor
      port: 22

```

## Strategy file format

Strategy is a set of orders to execute via SSH. The format is pretty simple:

```yaml
recon:
- CPU
- OS

orders:
- name: List all directories
  command: ls

- name: Current path
  command: pwd
```

`recon` field is responsible for specifing steps of gathering information about the target host.

`orders` is a list of commands that need to be executed on the target host.
