"""ClickHouse row conversion utilities."""

from enum import IntEnum
from decimal import Decimal
from typing import Any, Dict, List, Type, TypeVar, Union

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def row_to_dict(row: tuple, column_names: List[str]) -> Dict[str, Any]:
    """
    Convert a ClickHouse row tuple to a dictionary.

    Args:
        row: Row data as a tuple
        column_names: List of column names

    Returns:
        Dictionary mapping column names to values
    """
    result = {}
    for name, value in zip(column_names, row):
        if isinstance(value, Decimal):
            result[name] = format(value, 'f')
        else:
            result[name] = value
    return result


def convert_clickhouse_enum(enum_class: Type[IntEnum], value: Any) -> IntEnum | None:
    """
    Generic ClickHouse enum converter that handles multiple input formats.

    ClickHouse can return enums as:
    - Integer values (1, 2, 3, 4) - direct enum values
    - String names ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') - enum names
    - String numbers ('1', '2', '3', '4') - sometimes from queries

    Args:
        enum_class: The IntEnum class to convert to
        value: The value from ClickHouse to convert

    Returns:
        The converted enum instance

    Raises:
        ValueError: If the value cannot be converted to the enum
    """
    if value is None:
        return None

    # If it's already an enum instance, return as-is
    if isinstance(value, enum_class):
        return value

    # Try integer conversion first (most common case)
    if isinstance(value, int):
        try:
            return enum_class(value)
        except ValueError:
            pass

    # Try string to integer conversion
    if isinstance(value, str) and value.isdigit():
        try:
            return enum_class(int(value))
        except ValueError:
            pass

    # Try string name lookup (e.g., 'CRITICAL' -> AlertSeverity.CRITICAL)
    if isinstance(value, str):
        try:
            return enum_class[value.upper()]
        except KeyError:
            pass

    # If all else fails, raise a descriptive error
    available_values = [f"{e.name}({e.value})" for e in enum_class]
    raise ValueError(
        f"Cannot convert '{value}' (type: {type(value).__name__}) to {enum_class.__name__}. "
        f"Available values: {', '.join(available_values)}"
    )


def clickhouse_row_to_pydantic(
    model_class: Type[T],
    row_data: Union[Dict[str, Any], tuple],
    column_names: List[str] | None = None,
    enum_fields: Dict[str, Type[IntEnum]] | None = None,
) -> T:
    """
    Convert a ClickHouse row to a Pydantic model instance.

    Args:
        model_class: The Pydantic model class to create
        row_data: Row data as tuple or dict
        column_names: Column names (required if row_data is a tuple)
        enum_fields: Mapping of field names to enum classes for conversion

    Returns:
        Instance of the model class

    Raises:
        ValueError: If column_names not provided for tuple row_data
    """
    if isinstance(row_data, tuple):
        if not column_names:
            raise ValueError("column_names required when row_data is a tuple")
        row_dict = row_to_dict(row_data, column_names)
    else:
        row_dict = row_data.copy()

    # Convert enum fields if specified
    if enum_fields:
        for field_name, enum_class in enum_fields.items():
            if field_name in row_dict:
                row_dict[field_name] = convert_clickhouse_enum(enum_class, row_dict[field_name])

    # Create and return the Pydantic model instance
    return model_class(**row_dict)


def rows_to_pydantic_list(
    model_class: Type[T],
    rows: List[Union[Dict[str, Any], tuple]],
    column_names: List[str] | None = None,
    enum_fields: Dict[str, Type[IntEnum]] | None = None,
) -> List[T]:
    """
    Convert multiple ClickHouse rows to a list of Pydantic models.

    Args:
        model_class: The Pydantic model class to create
        rows: List of row data (tuples or dicts)
        column_names: Column names (required if rows contain tuples)
        enum_fields: Mapping of field names to enum classes for conversion

    Returns:
        List of model class instances
    """
    return [
        clickhouse_row_to_pydantic(model_class, row, column_names, enum_fields) for row in rows
    ]