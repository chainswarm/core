# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.3] - 2025-11-28

### Added

- Documentation and usage examples for `BaseMigrateSchema` class
- Example implementation pattern for project-specific `MigrateSchema` subclasses

## [0.1.2] - 2025-11-28

### Added

- Added unified `get_connection_params(network, database_prefix)` function for ClickHouse connections
  - Supports network-prefixed env vars (e.g., `TORUS_CLICKHOUSE_HOST`) with fallback to generic (`CLICKHOUSE_HOST`)
  - Database naming: `get_connection_params("torus", "analytics")` → database = `analytics_torus`
  - Works for all projects: data-pipeline, analytics-pipeline, chain-synthetics, subnet, etc.

## [0.1.1] - 2025-11-28

### Added

- Added `loguru` as a required dependency for logging

### Changed

- Removed linting from CI (black, ruff, mypy removed from dev dependencies)
- Simplified CI workflow to run only tests

### Fixed

- Fixed wheel build duplicate filename issue by removing redundant force-include config

## [0.1.0] - 2025-11-28

### Added

- Initial release of chainswarm-core package
- **Constants module** (`chainswarm_core.constants`):
  - `NetworkType` - blockchain network type classification (substrate, evm, utxo)
  - `Network` - enum of supported blockchain networks with helper methods
  - `AddressTypes` - classification of blockchain addresses (exchange, dex, mixer, etc.)
  - `TrustLevels` - address trust level classification
  - `RiskLevels` and `Severities` - risk/severity level enums
  - `PatternTypes` - detection pattern classifications
  - `DetectionMethods` - pattern detection method types
  - `PatternRoles` - role assignments for addresses in synthetic patterns
  - `AddressSubtypeRiskModifiers` - risk modifiers for address subtypes
  - Helper functions: `get_address_type_risk_level()`, `is_high_risk_address_type()`, etc.
- **Database module** (`chainswarm_core.db`):
  - `BaseRepository` - abstract base class for ClickHouse repositories
  - `ClientFactory` - thread-safe ClickHouse client factory with connection pooling
  - `BaseMigrateSchema` - base class for database migrations with core schema support
  - `create_database()` - create ClickHouse database if not exists
  - `truncate_table()` - truncate a ClickHouse table
  - `get_connection_params_from_env()` - get ClickHouse connection params from environment
  - `apply_schema_content()` - apply SQL schema from string content
  - `apply_schema_file()` - apply SQL schema from file path
  - `row_to_dict()` - convert ClickHouse row tuple to dictionary
  - `convert_clickhouse_enum()` - generic ClickHouse enum converter
  - `clickhouse_row_to_pydantic()` - convert ClickHouse row to Pydantic model
  - `rows_to_pydantic_list()` - convert multiple rows to Pydantic models
- **Schema module** (`chainswarm_core.schema`):
  - `get_core_schema_dir()` - get path to core SQL schema files
  - `list_core_schemas()` - list available core schema files
  - `read_core_schema()` - read core schema file content
  - Core SQL schemas included in package:
    - `core_assets.sql` - assets table schema
    - `core_asset_prices.sql` - asset prices table schema
    - `core_transfers.sql` - transfers table schema
    - `core_address_labels.sql` - address labels table schema
- **Logging module** (placeholder for future expansion)
- GitHub Actions CI/CD workflows
- Comprehensive test suite