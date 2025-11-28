"""Base repository class for ClickHouse data access."""

import time
from abc import ABC
from typing import Optional

import clickhouse_connect


class BaseRepository(ABC):
    """
    Abstract base class for ClickHouse repositories.

    Provides common functionality for all repository classes including
    client management and version generation for optimistic locking.
    """

    def __init__(
        self, client: clickhouse_connect.driver.Client, partition_id: Optional[int] = None
    ):
        """
        Initialize the repository with a ClickHouse client.

        Args:
            client: ClickHouse client instance
            partition_id: Optional partition ID for version generation
        """
        self.client = client
        self.partition_id = partition_id

    def _generate_version(self) -> int:
        """
        Generate a unique version number for optimistic locking.

        Uses microsecond timestamp with optional partition offset.

        Returns:
            Unique version number
        """
        base_version = int(time.time() * 1000000)
        if self.partition_id is not None:
            return base_version + self.partition_id
        return base_version

    @classmethod
    def schema(cls) -> str:
        """Return the schema file name for this repository."""
        pass

    @classmethod
    def table_name(cls) -> str:
        """Return the table name for this repository."""
        pass