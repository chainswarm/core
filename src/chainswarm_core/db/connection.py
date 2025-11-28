"""
Database connection utilities for ClickHouse.

This module provides functions for creating databases and managing connections.
"""

import os
from typing import Any

from clickhouse_connect import get_client
from clickhouse_connect.driver import Client


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


def get_connection_params_from_env(
    database_name: str,
    host_env: str = "CLICKHOUSE_HOST",
    port_env: str = "CLICKHOUSE_PORT",
    user_env: str = "CLICKHOUSE_USER",
    password_env: str = "CLICKHOUSE_PASSWORD",
    max_execution_time_env: str = "CLICKHOUSE_MAX_EXECUTION_TIME",
    max_query_size_env: str = "CLICKHOUSE_MAX_QUERY_SIZE",
) -> dict[str, Any]:
    """
    Get connection parameters from environment variables.
    
    This is a utility function to standardize how connection params are built.
    Each project may want to customize the database name format.
    
    Args:
        database_name: Database name (e.g., "analytics_torus", "synthetics_bittensor")
        host_env: Environment variable name for host
        port_env: Environment variable name for port
        user_env: Environment variable name for user
        password_env: Environment variable name for password
        max_execution_time_env: Environment variable name for max execution time
        max_query_size_env: Environment variable name for max query size
        
    Returns:
        Dict with connection parameters
    """
    return {
        "host": os.getenv(host_env, "localhost"),
        "port": os.getenv(port_env, "8123"),
        "database": database_name,
        "user": os.getenv(user_env, "default"),
        "password": os.getenv(password_env, ""),
        "max_execution_time": int(os.getenv(max_execution_time_env, "1800")),
        "max_query_size": int(os.getenv(max_query_size_env, "5000000")),
    }