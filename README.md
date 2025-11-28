# chainswarm-core

[![CI](https://github.com/chainswarm/core/actions/workflows/ci.yml/badge.svg)](https://github.com/chainswarm/core/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/chainswarm-core.svg)](https://badge.fury.io/py/chainswarm-core)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Shared constants and utilities for ChainSwarm blockchain analytics projects.

## Overview

`chainswarm-core` provides a single source of truth for:

- **Blockchain network definitions** - Network types, block times, native assets
- **Address classifications** - Address types, trust levels, risk mappings
- **Pattern detection constants** - Pattern types, detection methods, role classifications
- **Database utilities** - ClickHouse repository base class and row conversion utilities
- **Observability** - Logging, metrics (Prometheus), and graceful shutdown

This package eliminates code duplication across ChainSwarm projects including:
- `data-pipeline`
- `chain-synthetics`
- `analytics-pipeline`
- `ml-pipeline`
- `benchmark`
- `risk-scoring`

## Installation

```bash
pip install chainswarm-core
```

For development:
```bash
pip install chainswarm-core[dev]
```

## Quick Start

```python
from chainswarm_core import (
    AddressTypes,
    Network,
    NetworkType,
    RiskLevels,
    TrustLevels,
)

# Check network type
if Network.get_node_type("polkadot") == NetworkType.SUBSTRATE:
    print("Polkadot is a Substrate network")

# Get block time
block_time = Network.get_block_time("bitcoin")  # Returns 600 seconds

# Check address risk
from chainswarm_core.constants import get_address_type_risk_level, is_high_risk_address_type

risk = get_address_type_risk_level(AddressTypes.MIXER)  # Returns "critical"
is_risky = is_high_risk_address_type(AddressTypes.GAMBLING)  # Returns True
```

## Modules

### `chainswarm_core.constants.networks`

Network type classifications and blockchain network enum.

```python
from chainswarm_core.constants.networks import (
    NetworkType,      # SUBSTRATE, EVM, UTXO
    Network,          # Enum of supported networks
    substrate_networks,
    evm_networks,
    utxo_networks,
)

# Get native asset symbol
symbol = Network.get_native_asset_symbol("bittensor")  # Returns "TAO"
```

### `chainswarm_core.constants.addresses`

Address type and trust level classifications.

```python
from chainswarm_core.constants.addresses import (
    AddressTypes,     # EXCHANGE, DEX, MIXER, VALIDATOR, etc.
    TrustLevels,      # VERIFIED, COMMUNITY, OFFICIAL, etc.
    is_high_risk_address_type,
    is_trusted_address_type,
)
```

### `chainswarm_core.constants.risk`

Risk levels, severities, and risk mappings.

```python
from chainswarm_core.constants.risk import (
    RiskLevels,       # LOW, MEDIUM, HIGH, CRITICAL
    Severities,       # LOW, MEDIUM, HIGH, CRITICAL
    ADDRESS_TYPE_RISK_MAP,
    AddressSubtypeRiskModifiers,
    get_address_type_risk_level,
    get_subtype_risk_modifier,
)

# Get risk level for address type
risk = get_address_type_risk_level(AddressTypes.SCAM)  # Returns "critical"

# Get risk modifier for subtype
modifier = get_subtype_risk_modifier("uniswap_v3")  # Returns 0.8
```

### `chainswarm_core.constants.patterns`

Pattern detection types and role classifications.

```python
from chainswarm_core.constants.patterns import (
    PatternTypes,     # CYCLE, LAYERING_PATH, SMURFING_NETWORK, etc.
    DetectionMethods, # SCC_ANALYSIS, CYCLE_DETECTION, etc.
    PatternRoles,     # ATTACKER, MULE, HOT_WALLET, etc.
    MALICIOUS_ROLES,
    VICTIM_ROLES,
    BENIGN_ROLES,
    is_malicious_role,
    is_victim_role,
    is_benign_role,
)
```

### `chainswarm_core.db`

ClickHouse database utilities.

```python
from chainswarm_core.db import (
    BaseRepository,
    row_to_dict,
    convert_clickhouse_enum,
    clickhouse_row_to_pydantic,
    rows_to_pydantic_list,
)

# Create a repository
class MyRepository(BaseRepository):
    @classmethod
    def schema(cls) -> str:
        return "my_table.sql"
    
    @classmethod
    def table_name(cls) -> str:
        return "my_table"

# Convert rows to Pydantic models
from pydantic import BaseModel

class MyModel(BaseModel):
    id: int
    name: str

rows = [(1, "first"), (2, "second")]
columns = ["id", "name"]
models = rows_to_pydantic_list(MyModel, rows, columns)
```

### `chainswarm_core.observability`

Unified logging, metrics, and shutdown handling.

#### Logging

```python
from chainswarm_core.observability import (
    setup_logger,
    generate_correlation_id,
    get_correlation_id,
    set_correlation_id,
)

setup_logger("my-service")

correlation_id = generate_correlation_id()
set_correlation_id(correlation_id)

from loguru import logger
logger.info("Processing request")
```

#### Graceful Shutdown

```python
from chainswarm_core.observability import (
    terminate_event,
    install_shutdown_handlers,
)

install_shutdown_handlers()

while not terminate_event.is_set():
    process_batch()
```

#### Prometheus Metrics

```python
from chainswarm_core.observability import (
    setup_metrics,
    get_metrics_registry,
    MetricsRegistry,
    DURATION_BUCKETS,
)

PORT_MAPPING = {
    "my-service-indexer": 9101,
    "my-service-api": 9200,
}

metrics = setup_metrics("my-service-indexer", port_mapping=PORT_MAPPING)

blocks_counter = metrics.create_counter(
    "blocks_processed_total",
    "Total blocks processed",
    labelnames=["network"]
)
blocks_counter.labels(network="torus").inc()

processing_time = metrics.create_histogram(
    "block_processing_seconds",
    "Block processing duration",
    buckets=DURATION_BUCKETS
)
with processing_time.time():
    process_block()
```

#### Metrics Decorator

```python
from chainswarm_core.observability import manage_metrics

@manage_metrics(success_metric_name="task_success", failure_metric_name="task_failure")
def run_task():
    pass
```

## Migration Guide

### From project-local constants

**Before:**
```python
from packages.storage.constants import AddressTypes, RiskLevels
from packages.storage.repositories.base_repository import BaseRepository
```

**After:**
```python
from chainswarm_core import AddressTypes, RiskLevels, BaseRepository
```

### From project-local repository utils

**Before:**
```python
from packages.storage.repositories.utils import row_to_dict
```

**After:**
```python
from chainswarm_core.db import row_to_dict
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/chainswarm/core.git
cd core

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=chainswarm_core --cov-report=html

# Specific module
pytest tests/test_constants/test_networks.py -v
```

## CI/CD

- **CI**: Runs on every push and PR to `main`
  - Tests on Python 3.13
  
- **Publish**: Manual workflow dispatch to publish to PyPI
  - Requires version match in `pyproject.toml`
  - Creates GitHub release with tag

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Links

- [PyPI Package](https://pypi.org/project/chainswarm-core/)
- [GitHub Repository](https://github.com/chainswarm/core)
- [Changelog](CHANGELOG.md)