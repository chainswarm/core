"""
ClickHouse client factory with connection pooling and context management.

This module provides a ClientFactory class for managing ClickHouse connections
with proper resource cleanup and error handling.
"""

from contextlib import contextmanager
from typing import Iterator, Any

from clickhouse_connect import get_client
from clickhouse_connect.driver import Client
from clickhouse_connect.driver.exceptions import ClickHouseError
from loguru import logger


class ClientFactory:
    """
    Factory for creating ClickHouse client connections.
    
    Provides context manager for safe connection handling with automatic cleanup.
    
    Example:
        >>> factory = ClientFactory(connection_params)
        >>> with factory.client_context() as client:
        ...     result = client.query("SELECT 1")
    """
    
    client: Client = None

    def __init__(self, connection_params: dict[str, Any]) -> None:
        """
        Initialize ClientFactory with connection parameters.
        
        Args:
            connection_params: Dict with keys:
                - host: ClickHouse host
                - port: ClickHouse HTTP port
                - database: Target database name
                - user: Username
                - password: Password
                - max_execution_time: Query timeout (optional)
                - max_query_size: Max query size (optional)
        """
        self.connection_params = connection_params

    def _get_client(self) -> Client:
        """Create and return a new ClickHouse client."""
        self.client = get_client(
            host=self.connection_params['host'],
            port=int(self.connection_params['port']),
            username=self.connection_params['user'],
            password=self.connection_params['password'],
            database=self.connection_params['database'],
            settings={
                'output_format_parquet_compression_method': 'zstd',
                'async_insert': 0,
                'wait_for_async_insert': 1,
                'max_execution_time': self.connection_params.get('max_execution_time', 3600),
                'max_query_size': self.connection_params.get('max_query_size', 5000000)
            }
        )
        return self.client

    def _get_client_default_database(self) -> Client:
        """Create a client connected to the 'default' database."""
        client = get_client(
            host=self.connection_params['host'],
            port=int(self.connection_params['port']),
            username=self.connection_params['user'],
            password=self.connection_params['password'],
            database='default',
            settings={
                'output_format_parquet_compression_method': 'zstd',
                'max_execution_time': self.connection_params.get('max_execution_time', 3600),
                'max_query_size': self.connection_params.get('max_query_size', 5000000),
                'enable_http_compression': 1,
                'send_progress_in_http_headers': 0,
                'http_headers_progress_interval_ms': 1000,
                'http_zlib_compression_level': 3,
            },
            client_query_params={
                'default_format': 'JSON',
                'result_format': 'JSON'
            }
        )
        return client

    @contextmanager
    def client_context(self) -> Iterator[Client]:
        """
        Context manager for safe client usage with automatic cleanup.
        
        Yields:
            Client: ClickHouse client connection
            
        Raises:
            ClickHouseError: If a ClickHouse operation fails
        """
        client = self._get_client()
        try:
            yield client
        except ClickHouseError as e:
            import traceback
            logger.error(
                "ClickHouse error",
                error=e,
                traceback=traceback.format_exc(),
            )
            raise
        finally:
            if client:
                client.close()