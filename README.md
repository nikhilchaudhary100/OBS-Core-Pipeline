# OBS-Core-Pipeline

A Python-based telemetry engine for parsing unstructured sensor logs, performing diagnostic anomaly detection, and routing malformed data streams.

## Architecture & Core Features

* **Multi-Tier Semantic Validation:** Rejects superficial structural validation. Checks for null values, hardware `ERR_` flags, and missing numeric data before allowing records into the analytics stream.
* **Dead Letter Queue (DLQ) Isolation:** Implements graceful degradation. Instead of crashing on malformed strings or silently dropping them, corrupted records are serialized with their root-cause error classification into a durable JSONL file (`data/dead_letters/dlq.json`).
* **O(1) Memory Stream Processing:** Evaluates incoming telemetry line-by-line via stream iterators, guaranteeing flat memory usage regardless of input file size.
* **Dynamic CLI Wrapper:** Built with `argparse` for dynamic target selection, sensor isolation, and performance benchmarking.

## Installation

Clone the repository and ensure you are running Python 3.10+. No heavy external dependencies are required for the core engine.

```bash
git clone [https://github.com/nikhilchaudhary100/OBS-Core-Pipeline.git](https://github.com/nikhilchaudhary100/OBS-Core-Pipeline.git)

cd OBS-Core-Pipeline
```

## Usage
The pipeline is executed via a synchronous CLI entry point.

**Standard Execution**:
```bash
python -m src.cli --file data/raw_logs/sensor_data.log --detect-spikes --sensor SENSOR_99
```
## Testing
This project enforces clean DataOps standards and utilizes pytest to verify happy paths and robust DLQ error-handling logic.
```bash
python -m pytest
```

## Project Structure
```text
OBS-Core-Pipeline/
├── data/
│   ├── dead_letters/
│   │   └── dlq.json            # Durable storage for isolated, corrupted records
│   └── raw_logs/
│       └── sensor_data.log     # The chaotic, raw input telemetry stream
├── src/
│   ├── __init__.py
│   ├── analyzer.py             # Stream processing engine for diagnostic state counters
│   ├── cli.py                  # Synchronous CLI wrapper and main execution entry point
│   ├── error_handler.py        # The mechanical arm routing failures to the DLQ
│   ├── generator.py            # Simulates chaos by injecting deliberate anomalies
│   └── parser.py               # Pre-compiled Regex and multi-tier semantic validation
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   └── test_parser.py          # Pytest suite verifying validation and DLQ routing logic
├── .gitignore                  # Enforces clean DataOps by ignoring caches
├── LICENSE
└── README.md
```
