# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
  - `row_to_dict()` - convert ClickHouse row tuple to dictionary
  - `convert_clickhouse_enum()` - generic ClickHouse enum converter
  - `clickhouse_row_to_pydantic()` - convert ClickHouse row to Pydantic model
  - `rows_to_pydantic_list()` - convert multiple rows to Pydantic models
- **Logging module** (placeholder for future expansion)
- GitHub Actions CI/CD workflows
- Comprehensive test suite