![Alt text](/docs/logo/full_logo_dark.png?raw=true#gh-dark-mode-only)
![Alt text](/docs/logo/full_logo.png?raw=true#gh-light-mode-only)

---
A library for mass execution of ssh commands on remote machines fleet. 

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

## Running strategy

```
python3 -m kornet <strategy_file.yml> <fleet_file.yml> <group>
```

**strategy file** - yaml strategy file described above

**fleet file** - yaml fleet file described above

**group** - group to run the strategy on
