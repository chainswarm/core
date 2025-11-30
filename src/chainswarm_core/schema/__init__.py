"""
Schema resources for chainswarm-core.

NOTE: Core SQL schemas have been removed as of v0.1.10.
Each project (data-pipeline, analytics-pipeline, etc.) should maintain
its own schema definitions to avoid coupling and schema conflicts.

This module is kept for backward compatibility but functions are deprecated.
"""

from pathlib import Path


def get_core_schema_dir() -> Path:
    """
    DEPRECATED: Core schemas have been removed in v0.1.10.
    
    Each project should maintain its own schema definitions.
    
    Returns:
        Path to the (now empty/non-existent) 'core' schema directory
    """
    return Path(__file__).parent / "core"


def list_core_schemas() -> list[str]:
    """
    DEPRECATED: Core schemas have been removed in v0.1.10.
    
    Returns:
        Empty list (no core schemas bundled)
    """
    return []


def read_core_schema(schema_name: str) -> str:
    """
    DEPRECATED: Core schemas have been removed in v0.1.10.
    
    Args:
        schema_name: Schema file name
        
    Raises:
        FileNotFoundError: Always raised (no core schemas exist)
    """
    raise FileNotFoundError(
        f"Core schema '{schema_name}' not found. "
        "Core schemas have been removed in v0.1.10. "
        "Each project should maintain its own schema definitions."
    )