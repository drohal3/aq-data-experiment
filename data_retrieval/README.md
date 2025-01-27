# Data retrieval experiments
To start a data retrieval, run one of the Python scripts located in [experiments](./experiments) directory and wait until the retrieval is finished.

Some of the experiments (recent data retrieval) might require data simulation to be running, others (historical data retrievals) might require some time to pass since the simulation has finished.

> **Note: modify constants (in capital) in the retrieval scripts before running them. They are self-describing.**

Run python scripts from this directory .i.e.

```python
python3 experiments/historical_1d.py
```

The metrics are recorded in [local](../local) directory located in the project's root directory (parent of the current directory).

> Make sure the [local](../local) directory in the repository root exists before the retrival script is run! `mkdir ../local`