# Analysis
> make sure the relevant data retrieval scripts have been run before analyzing and plotting metrics

To plot data, run one of the Python scripts located in subdirectories.

There are 3 main metrics analyzed:
- elapsed: execution time
- items: number of retrieved items
- requests: number of requests

...and 3 types of retrievals analyzed
- historical data: 1 day long time-series data segments
- recent 1m (short recent data): 1 minute long time-series data segments of recent data / real-time data
- recent 30m (long recent data): 30 minutes long time-series data segments of recent data / real0time data

> **Note:** verify and modify the paths in the scripts to lead to existing directories where data recorder from the experiments is saved

i.e. to plot elapsed times from short recent data, run

```python
python3 recent_1_m_all_atr/elapsed.py
```