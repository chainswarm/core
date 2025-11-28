"""Tests for chainswarm_core.db.utils module."""

from enum import IntEnum

import pytest
from pydantic import BaseModel

from chainswarm_core.db.utils import (
    clickhouse_row_to_pydantic,
    convert_clickhouse_enum,
    row_to_dict,
    rows_to_pydantic_list,
)


class MockSeverity(IntEnum):
    """Mock severity enum for testing."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class MockModel(BaseModel):
    """Mock Pydantic model for testing."""

    id: int
    name: str
    value: float


class MockModelWithEnum(BaseModel):
    """Mock Pydantic model with enum for testing."""

    id: int
    severity: MockSeverity


class TestRowToDict:
    """Tests for row_to_dict function."""

    def test_converts_tuple_to_dict(self):
        """Test basic tuple to dict conversion."""
        row = (1, "test", 3.14)
        columns = ["id", "name", "value"]
        result = row_to_dict(row, columns)

        assert result == {"id": 1, "name": "test", "value": 3.14}

    def test_handles_empty_row(self):
        """Test empty row conversion."""
        row = ()
        columns = []
        result = row_to_dict(row, columns)

        assert result == {}

    def test_handles_none_values(self):
        """Test row with None values."""
        row = (1, None, 3.14)
        columns = ["id", "name", "value"]
        result = row_to_dict(row, columns)

        assert result == {"id": 1, "name": None, "value": 3.14}


class TestConvertClickhouseEnum:
    """Tests for convert_clickhouse_enum function."""

    def test_returns_none_for_none(self):
        """Test None input returns None."""
        result = convert_clickhouse_enum(MockSeverity, None)
        assert result is None

    def test_returns_existing_enum(self):
        """Test already enum value is returned as-is."""
        result = convert_clickhouse_enum(MockSeverity, MockSeverity.HIGH)
        assert result == MockSeverity.HIGH

    def test_converts_integer_to_enum(self):
        """Test integer conversion."""
        result = convert_clickhouse_enum(MockSeverity, 3)
        assert result == MockSeverity.HIGH

    def test_converts_string_digit_to_enum(self):
        """Test string digit conversion."""
        result = convert_clickhouse_enum(MockSeverity, "3")
        assert result == MockSeverity.HIGH

    def test_converts_string_name_to_enum(self):
        """Test string name conversion."""
        result = convert_clickhouse_enum(MockSeverity, "HIGH")
        assert result == MockSeverity.HIGH

    def test_converts_lowercase_name_to_enum(self):
        """Test lowercase string name conversion."""
        result = convert_clickhouse_enum(MockSeverity, "high")
        assert result == MockSeverity.HIGH

    def test_raises_for_invalid_value(self):
        """Test invalid value raises ValueError."""
        with pytest.raises(ValueError, match="Cannot convert"):
            convert_clickhouse_enum(MockSeverity, "invalid")

    def test_raises_for_invalid_integer(self):
        """Test invalid integer raises ValueError."""
        with pytest.raises(ValueError, match="Cannot convert"):
            convert_clickhouse_enum(MockSeverity, 999)


class TestClickhouseRowToPydantic:
    """Tests for clickhouse_row_to_pydantic function."""

    def test_converts_dict_to_model(self):
        """Test dict row to model conversion."""
        row_dict = {"id": 1, "name": "test", "value": 3.14}
        result = clickhouse_row_to_pydantic(MockModel, row_dict)

        assert result.id == 1
        assert result.name == "test"
        assert result.value == 3.14

    def test_converts_tuple_to_model(self):
        """Test tuple row to model conversion."""
        row_tuple = (1, "test", 3.14)
        columns = ["id", "name", "value"]
        result = clickhouse_row_to_pydantic(MockModel, row_tuple, columns)

        assert result.id == 1
        assert result.name == "test"
        assert result.value == 3.14

    def test_raises_without_columns_for_tuple(self):
        """Test tuple without columns raises ValueError."""
        row_tuple = (1, "test", 3.14)
        with pytest.raises(ValueError, match="column_names required"):
            clickhouse_row_to_pydantic(MockModel, row_tuple)

    def test_converts_enum_fields(self):
        """Test enum field conversion."""
        row_dict = {"id": 1, "severity": 3}
        result = clickhouse_row_to_pydantic(
            MockModelWithEnum, row_dict, enum_fields={"severity": MockSeverity}
        )

        assert result.id == 1
        assert result.severity == MockSeverity.HIGH

    def test_converts_string_enum_fields(self):
        """Test string enum field conversion."""
        row_dict = {"id": 1, "severity": "CRITICAL"}
        result = clickhouse_row_to_pydantic(
            MockModelWithEnum, row_dict, enum_fields={"severity": MockSeverity}
        )

        assert result.severity == MockSeverity.CRITICAL


class TestRowsToPydanticList:
    """Tests for rows_to_pydantic_list function."""

    def test_converts_list_of_dicts(self):
        """Test list of dict rows conversion."""
        rows = [
            {"id": 1, "name": "first", "value": 1.0},
            {"id": 2, "name": "second", "value": 2.0},
        ]
        result = rows_to_pydantic_list(MockModel, rows)

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].name == "second"

    def test_converts_list_of_tuples(self):
        """Test list of tuple rows conversion."""
        rows = [
            (1, "first", 1.0),
            (2, "second", 2.0),
        ]
        columns = ["id", "name", "value"]
        result = rows_to_pydantic_list(MockModel, rows, columns)

        assert len(result) == 2
        assert result[0].name == "first"
        assert result[1].value == 2.0

    def test_handles_empty_list(self):
        """Test empty list returns empty list."""
        result = rows_to_pydantic_list(MockModel, [])
        assert result == []

    def test_converts_with_enum_fields(self):
        """Test list conversion with enum fields."""
        rows = [
            {"id": 1, "severity": 1},
            {"id": 2, "severity": "HIGH"},
        ]
        result = rows_to_pydantic_list(
            MockModelWithEnum, rows, enum_fields={"severity": MockSeverity}
        )

        assert result[0].severity == MockSeverity.LOW
        assert result[1].severity == MockSeverity.HIGH