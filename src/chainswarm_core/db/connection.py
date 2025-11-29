"""
Database connection utilities for ClickHouse.

This module provides functions for creating databases and managing connections.
"""

import os
from typing import Any

from clickhouse_connect import get_client
from clickhouse_connect.driver import Client


def get_connection_params(
    network: str | None = None,
    database_prefix: str | None = None,
) -> dict[str, Any]:
    """
    Get ClickHouse connection parameters from environment variables.
    
    Environment Variables (always used, no network prefixes):
        - CLICKHOUSE_HOST (default: localhost)
        - CLICKHOUSE_PORT (default: 8123)
        - CLICKHOUSE_DB (default: default)
        - CLICKHOUSE_USER (default: user)
        - CLICKHOUSE_PASSWORD (default: password1234)
        - CLICKHOUSE_MAX_EXECUTION_TIME (default: 1800)
        - CLICKHOUSE_MAX_QUERY_SIZE (default: 5000000)
    
    Args:
        network: Network name (e.g., 'torus', 'bitcoin'). Used for database name.
        database_prefix: Prefix for database name (e.g., 'analytics', 'synthetics').
    
    Returns:
        Dict with connection params: host, port, database, user, password,
        max_execution_time, max_query_size
    
    Database naming:
        - prefix + network: database = f"{prefix}_{network}" (e.g., "analytics_torus")
        - network only: database = network (e.g., "torus")
        - neither: database = CLICKHOUSE_DB env var or "default"
    
    Examples:
        # data-pipeline: database = "torus"
        get_connection_params(network="torus")
        
        # analytics-pipeline: database = "analytics_torus"
        get_connection_params(network="torus", database_prefix="analytics")
        
        # chain-synthetics: database = "synthetics_torus"
        get_connection_params(network="torus", database_prefix="synthetics")
        
        # benchmark: database = "benchmark_torus"
        get_connection_params(network="torus", database_prefix="benchmark")
        
        # No network (uses CLICKHOUSE_DB or "default")
        get_connection_params()
    """
    # Build database name
    if database_prefix and network:
        database = f"{database_prefix}_{network}"
    elif network:
        database = network
    else:
        database = os.getenv("CLICKHOUSE_DB", "default")
    
    return {
        "host": os.getenv("CLICKHOUSE_HOST", "localhost"),
        "port": os.getenv("CLICKHOUSE_PORT", "8123"),
        "database": database,
        "user": os.getenv("CLICKHOUSE_USER", "user"),
        "password": os.getenv("CLICKHOUSE_PASSWORD", "password1234"),
        "max_execution_time": int(os.getenv("CLICKHOUSE_MAX_EXECUTION_TIME", "1800")),
        "max_query_size": int(os.getenv("CLICKHOUSE_MAX_QUERY_SIZE", "5000000")),
    }


def create_database(connection_params: dict[str, Any]) -> None:
    """
    Create a database if it doesn't exist.
    
    Connects to the 'default' database and creates the target database.
    
    Args:
        connection_params: Dict with keys:
            - host: ClickHouse host
            - port: ClickHouse HTTP port
            - database: Target database name to create
            - user: Username
            - password: Password
    """
    client = get_client(
        host=connection_params['host'],
        port=int(connection_params['port']),
        username=connection_params['user'],
        password=connection_params['password'],
        database='default',
        settings={
            'enable_http_compression': 1,
            'send_progress_in_http_headers': 0,
            'http_headers_progress_interval_ms': 1000,
            'http_zlib_compression_level': 3,
            'max_execution_time': connection_params.get('max_execution_time', 3600),
            'max_query_size': connection_params.get('max_query_size', 5000000)
        }
    )

    client.command(f"CREATE DATABASE IF NOT EXISTS {connection_params['database']}")
    client.close()


def truncate_table(client: Client, table_name: str) -> None:
    """
    Truncate a table if it exists.
    
    Args:
        client: ClickHouse client connection
        table_name: Name of table to truncate
    """
    client.command(f"TRUNCATE TABLE IF EXISTS {table_name}")