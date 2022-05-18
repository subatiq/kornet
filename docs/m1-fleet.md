# Fleet

Fleet is a collection of hosts that you want to work with. It's specified either in a `.yaml` file, or as a `dict` when using Kornet as a package

## Hosts file format

You need to specify hosts and their groups. Groups so far can store only simple SSH configurations (username, password and port). Each host can override these values by specifying certain fields.

```yaml
hosts:
- ip: 192.168.0.2
  groups: [office]
- ip: 192.168.0.3
  groups: [office]

groups:
  office:
    ssh:
      username: root
      password: toor
      port: 22

```

When executing a strategy (explained below), user chooses a group to execute on. Then, ssh configuration of a group is applied to every host in the list. 

### Overriding group's options

Sometimes hosts do not conform to a group's settings. And that's a good thing for passwords. To override certain group configuration on the hosts, just explicitly state it in the same format for specific hosts.

```yaml hl_lines="3 4 7-9"
hosts:
- ip: 192.168.0.2
  ssh:
    port: 5022
  groups: [office]
- ip: 192.168.0.3
  ssh:
    username: user
    password: password 
  groups: [office]

groups:
  office:
    ssh:
      username: root
      password: toor
      port: 22
```

In the example, host 192.168.0.2 will try to connect to port 5022 instead of 22 with group credentials (root:toor), and 192.168.0.3 will connect to port 22, as specified in the group with it's own credentials (user:password).

