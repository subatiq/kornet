# Strategies

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

`recon` field is responsible for specifing steps of gathering information about the target host, while `orders` is a list of commands that need to be executed on the target host.


## Orders

Orders are simple terminal commands with additional options.

```python
class Order(Model):
    name: Optional[str] = None
    command: str
    silent: bool = False
    outcome: Optional[OrderOutcome] = None
```

### Configuration

Name just specifies a human-readable label of an order, it does not affect anything

Silent option can be switched on and off to show/hide the output of the command execution. Can be handy if output is too large.


```yaml
orders:
- name: Sample order
- command: apt-install vim
- silent: yes
```

### Outcome

Outcome is an abstraction over the result of the order execution. If order is executed successfuly, here will be information about it

```python
class OrderOutcome(Model):
    code: int
    outputs: list[str]
    errors: str
```

Code - exit code of the command, outputs - list of lines outputted by the command, errors - plain error string if anything went wrong.

