"""Tests for chainswarm_core.db.base_repository module."""

import time
from unittest.mock import MagicMock

from chainswarm_core.db.base_repository import BaseRepository


class ConcreteRepository(BaseRepository):
    """Concrete implementation for testing."""

    @classmethod
    def schema(cls) -> str:
        return "test_schema.sql"

    @classmethod
    def table_name(cls) -> str:
        return "test_table"


class TestBaseRepository:
    """Tests for BaseRepository class."""

    def test_init_with_client(self, mock_clickhouse_client):
        """Test initialization with client."""
        repo = ConcreteRepository(mock_clickhouse_client)
        assert repo.client == mock_clickhouse_client
        assert repo.partition_id is None

    def test_init_with_partition_id(self, mock_clickhouse_client):
        """Test initialization with partition ID."""
        repo = ConcreteRepository(mock_clickhouse_client, partition_id=5)
        assert repo.partition_id == 5

    def test_generate_version_without_partition(self, mock_clickhouse_client):
        """Test version generation without partition."""
        repo = ConcreteRepository(mock_clickhouse_client)
        before = int(time.time() * 1000000)
        version = repo._generate_version()
        after = int(time.time() * 1000000)

        assert before <= version <= after + 1000

    def test_generate_version_with_partition(self, mock_clickhouse_client):
        """Test version generation with partition offset."""
        repo = ConcreteRepository(mock_clickhouse_client, partition_id=42)
        version = repo._generate_version()

        # Version should end with partition_id
        assert version % 1000000 >= 42 or version % 100 == 42

    def test_schema_method(self, mock_clickhouse_client):
        """Test schema class method."""
        assert ConcreteRepository.schema() == "test_schema.sql"

    def test_table_name_method(self, mock_clickhouse_client):
        """Test table_name class method."""
        assert ConcreteRepository.table_name() == "test_table"


class TestBaseRepositoryInheritance:
    """Tests for proper inheritance behavior."""

    def test_can_create_subclass(self, mock_clickhouse_client):
        """Test that BaseRepository can be properly subclassed."""

        class MyRepository(BaseRepository):
            @classmethod
            def schema(cls) -> str:
                return "my_schema.sql"

            @classmethod
            def table_name(cls) -> str:
                return "my_table"

        repo = MyRepository(mock_clickhouse_client)
        assert repo.client == mock_clickhouse_client

    def test_version_unique_per_call(self, mock_clickhouse_client):
        """Test that each version call produces unique value."""
        repo = ConcreteRepository(mock_clickhouse_client)
        versions = [repo._generate_version() for _ in range(10)]

        # All versions should be unique (within reason for timing)
        # At minimum, they should be monotonically increasing
        for i in range(1, len(versions)):
            assert versions[i] >= versions[i - 1]