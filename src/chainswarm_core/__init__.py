"""ChainSwarm Core - Shared constants and utilities for ChainSwarm projects."""

__version__ = "0.1.0"

# Core constant that all projects use
DEFAULT_ASSET_CONTRACT = "native"

# Re-export commonly used items for convenience
from chainswarm_core.constants import (
    AddressTypes,
    Network,
    NetworkType,
    RiskLevels,
    Severities,
    TrustLevels,
)
from chainswarm_core.db import (
    BaseRepository,
    BaseMigrateSchema,
    ClientFactory,
    create_database,
    get_connection_params_from_env,
)
from chainswarm_core.schema import (
    get_core_schema_dir,
    list_core_schemas,
    read_core_schema,
)

__all__ = [
    "__version__",
    "DEFAULT_ASSET_CONTRACT",
    # Constants
    "NetworkType",
    "Network",
    "AddressTypes",
    "TrustLevels",
    "RiskLevels",
    "Severities",
    # Database
    "BaseRepository",
    "BaseMigrateSchema",
    "ClientFactory",
    "create_database",
    "get_connection_params_from_env",
    # Schema utilities
    "get_core_schema_dir",
    "list_core_schemas",
    "read_core_schema",
]