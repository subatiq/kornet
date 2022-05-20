# Usage

## Running a strategy in CLI

```
kornet run <strategy_file.yml> <fleet_file.yml> <group>
```

**strategy file** - yaml strategy file described is Strategies section

**fleet file** - yaml fleet file described in Fleet section

**group** - group to run the strategy on


## Fast recon

```bash
kornet recon <recon catalog entry> <username>@<hostname> --port 22
```

Example:

```bash
python3 -m kornet recon CPU user@192.168.0.2
```

Result:

```
Results:
cpu:
  arch: x86_64
  cores: 8
  model: Intel(R) Core(TM) i5-8265U CPU @ 1.60GHz
```