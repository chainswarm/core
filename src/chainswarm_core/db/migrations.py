"""
Schema migration utilities for ClickHouse.

This module provides a base class for managing ClickHouse schema migrations.
Each project defines its own schema files and migration logic.
"""

import io
from pathlib import Path
from typing import Iterable

from clickhouse_connect.driver import Client
from loguru import logger


def _split_clickhouse_sql(sql_text: str) -> Iterable[str]:
    """
    Split a SQL file into individual statements.
    
    Handles:
    - Line comments (-- ...)
    - Statement separation by semicolons
    
    Args:
        sql_text: Raw SQL content
        
    Yields:
        Individual SQL statements
    """
    cleaned = io.StringIO()
    for line in sql_text.splitlines():
        if line.strip().startswith("--"):
            continue
        parts = line.split("--", 1)
        cleaned.write(parts[0] + "\n")

    buf = []
    for ch in cleaned.getvalue():
        if ch == ";":
            stmt = "".join(buf).strip()
            if stmt:
                yield stmt
            buf = []
        else:
            buf.append(ch)

    tail = "".join(buf).strip()
    if tail:
        yield tail


def apply_schema_content(client: Client, sql_content: str) -> None:
    """
    Apply SQL statements from a content string.
    
    Args:
        client: ClickHouse client connection
        sql_content: SQL content with possibly multiple statements
    """
    for stmt in _split_clickhouse_sql(sql_content):
        client.command(stmt)


def apply_schema_file(client: Client, schema_path: Path) -> None:
    """
    Apply SQL statements from a file path.
    
    Args:
        client: ClickHouse client connection
        schema_path: Path to SQL schema file
        
    Raises:
        FileNotFoundError: If schema file doesn't exist
    """
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    sql_content = schema_path.read_text(encoding="utf-8")
    apply_schema_content(client, sql_content)


def apply_schema(client: Client, schema_name: str, schema_dir: Path) -> None:
    """
    Apply a named schema from a directory.
    
    Args:
        client: ClickHouse client connection
        schema_name: Name of the schema file (e.g., "core_transfers.sql")
        schema_dir: Directory containing schema files
        
    Raises:
        FileNotFoundError: If schema file doesn't exist
    """
    schema_path = schema_dir / schema_name
    apply_schema_file(client, schema_path)


class BaseMigrateSchema:
    """
    Base schema migration manager.
    
    Subclass in each project to define project-specific schemas.
    Each project maintains its own schema files and migration logic.
    
    Example:
        >>> class MigrateSchema(BaseMigrateSchema):
        ...     core_schemas = [
        ...         "core_transfers.sql",
        ...         "core_money_flows.sql",
        ...     ]
        ...
        ...     def get_project_schema_dir(self) -> Path:
        ...         return Path(__file__).parent / "schema"
        ...
        ...     def run_data_migrations(self) -> None:
        ...         self.run_schemas_from_dir(
        ...             self.core_schemas,
        ...             self.get_project_schema_dir()
        ...         )
    """
    
    def __init__(self, client: Client):
        """
        Initialize migration manager.
        
        Args:
            client: ClickHouse client connection
        """
        self.client = client
    
    def run_schemas_from_dir(
        self,
        schema_files: list[str],
        schema_dir: Path
    ) -> None:
        """
        Run migrations from a directory.
        
        Args:
            schema_files: List of schema file names to apply
            schema_dir: Directory containing the schema files
        """
        for schema_file in schema_files:
            schema_path = schema_dir / schema_file
            try:
                if schema_path.exists():
                    apply_schema_file(self.client, schema_path)
                    logger.info(f"Applied schema: {schema_file}")
                else:
                    logger.warning(f"Schema not found: {schema_path}")
            except Exception as e:
                logger.error(f"Failed to apply schema {schema_file}: {e}")
                raise