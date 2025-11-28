"""
Schema resources for chainswarm-core.

This module provides utilities for accessing bundled SQL schema files.
"""

from pathlib import Path


def get_core_schema_dir() -> Path:
    """
    Get path to core schemas bundled with chainswarm-core.
    
    Returns:
        Path to the 'core' schema directory
    """
    return Path(__file__).parent / "core"


def list_core_schemas() -> list[str]:
    """
    List all available core schema files.
    
    Returns:
        List of schema file names (e.g., ["core_assets.sql", "core_transfers.sql"])
    """
    schema_dir = get_core_schema_dir()
    if not schema_dir.exists():
        return []
    return [f.name for f in schema_dir.iterdir() if f.name.endswith(".sql")]


def read_core_schema(schema_name: str) -> str:
    """
    Read content of a core schema file.
    
    Args:
        schema_name: Schema file name (e.g., "core_assets.sql")
        
    Returns:
        SQL content as string
        
    Raises:
        FileNotFoundError: If schema file doesn't exist
    """
    schema_path = get_core_schema_dir() / schema_name
    if not schema_path.exists():
        raise FileNotFoundError(f"Core schema not found: {schema_name}")
    return schema_path.read_text(encoding="utf-8")