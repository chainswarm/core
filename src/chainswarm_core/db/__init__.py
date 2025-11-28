"""Database utilities for ClickHouse repositories."""

from chainswarm_core.db.base_repository import BaseRepository
from chainswarm_core.db.client_factory import ClientFactory
from chainswarm_core.db.connection import (
    create_database,
    get_connection_params,
    get_connection_params_from_env,
    truncate_table,
)
from chainswarm_core.db.migrations import (
    BaseMigrateSchema,
    apply_schema_content,
    apply_schema_file,
)
from chainswarm_core.db.utils import (
    clickhouse_row_to_pydantic,
    convert_clickhouse_enum,
    row_to_dict,
    rows_to_pydantic_list,
)

__all__ = [
    # Repository
    "BaseRepository",
    # Client factory
    "ClientFactory",
    # Connection utilities
    "create_database",
    "truncate_table",
    "get_connection_params",
    "get_connection_params_from_env",  # Legacy, use get_connection_params
    # Migrations
    "BaseMigrateSchema",
    "apply_schema_content",
    "apply_schema_file",
    # Row utilities
    "row_to_dict",
    "convert_clickhouse_enum",
    "clickhouse_row_to_pydantic",
    "rows_to_pydantic_list",
]