"""
Schema migration utilities for ClickHouse.

This module provides a base class for managing ClickHouse schema migrations,
with support for bundled core schemas and project-specific schemas.
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
    
    Subclass in each project to add project-specific migrations while
    reusing core migrations from chainswarm-core.
    
    Example:
        >>> class MigrateSchema(BaseMigrateSchema):
        ...     def run_project_migrations(self):
        ...         local_dir = Path(__file__).parent.parent / "schema"
        ...         self.run_schemas_from_dir([
        ...             "my_table.sql",
        ...         ], local_dir)
    """
    
    # Core schemas bundled with chainswarm-core
    CORE_SCHEMAS = [
        "core_assets.sql",
        "core_asset_prices.sql",
        "core_transfers.sql",
        "core_address_labels.sql",
    ]
    
    def __init__(self, client: Client):
        """
        Initialize migration manager.
        
        Args:
            client: ClickHouse client connection
        """
        self.client = client
    
    def get_core_schema_dir(self) -> Path:
        """
        Get path to core schemas bundled with chainswarm-core.
        
        Returns:
            Path to the core schema directory
        """
        return Path(__file__).parent.parent / "schema" / "core"
    
    def run_core_migrations(self) -> None:
        """
        Run shared core migrations from chainswarm-core package.
        
        These are the base tables needed by most projects:
        - core_assets
        - core_asset_prices  
        - core_transfers
        - core_address_labels
        """
        schema_dir = self.get_core_schema_dir()
        
        for schema_name in self.CORE_SCHEMAS:
            schema_path = schema_dir / schema_name
            try:
                if schema_path.exists():
                    apply_schema_file(self.client, schema_path)
                    logger.info(f"Applied core schema: {schema_name}")
                else:
                    logger.warning(f"Core schema not found: {schema_path}")
            except Exception as e:
                logger.error(f"Failed to apply core schema {schema_name}: {e}")
                raise
    
    def run_schemas_from_dir(
        self, 
        schema_files: list[str], 
        schema_dir: Path
    ) -> None:
        """
        Run migrations from a local directory (project-specific schemas).
        
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