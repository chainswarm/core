"""Pytest configuration and fixtures for chainswarm_core tests."""

from enum import IntEnum
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel


class MockSeverity(IntEnum):
    """Mock severity enum for testing enum conversion."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class MockModel(BaseModel):
    """Mock Pydantic model for testing row conversion."""

    id: int
    name: str
    value: float


class MockModelWithEnum(BaseModel):
    """Mock Pydantic model with enum for testing."""

    id: int
    severity: MockSeverity


@pytest.fixture
def mock_clickhouse_client():
    """Create a mock ClickHouse client."""
    client = MagicMock()
    client.query = MagicMock()
    client.insert = MagicMock()
    return client


@pytest.fixture
def sample_row_tuple():
    """Sample row as tuple."""
    return (1, "test", 3.14)


@pytest.fixture
def sample_column_names():
    """Column names for sample row."""
    return ["id", "name", "value"]


@pytest.fixture
def sample_row_dict():
    """Sample row as dictionary."""
    return {"id": 1, "name": "test", "value": 3.14}