# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.10] - 2025-11-30

### Removed

- **Schema module** (`chainswarm_core.schema`):
  - Removed all core SQL schema files (`core_transfers.sql`, `core_assets.sql`, `core_asset_prices.sql`, `core_address_labels.sql`)
  - Each project (data-pipeline, analytics-pipeline, etc.) should now maintain its own schema definitions
  - This avoids schema coupling and conflicts between different projects with different column requirements
  - Functions `get_core_schema_dir()`, `list_core_schemas()`, `read_core_schema()` are now deprecated and return empty/raise errors

## [0.1.9] - 2025-11-29

### Changed

- **Database connection** (`chainswarm_core.db.get_connection_params`):
  - Simplified ClickHouse connection parameter resolution - removed network-prefixed env var fallback
  - Environment variables now use fixed names (no more `TORUS_CLICKHOUSE_HOST` fallback):
    - `CLICKHOUSE_HOST` (default: `localhost`)
    - `CLICKHOUSE_PORT` (default: `8123`)
    - `CLICKHOUSE_DB` (default: `default`)
    - `CLICKHOUSE_USER` (default: `user`)
    - `CLICKHOUSE_PASSWORD` (default: `password1234`)
    - `CLICKHOUSE_MAX_EXECUTION_TIME` (default: `1800`)
    - `CLICKHOUSE_MAX_QUERY_SIZE` (default: `5000000`)
  - Database name is now determined solely by `network` and `database_prefix` parameters:
    - `get_connection_params(network="torus", database_prefix="analytics")` → `analytics_torus`
    - `get_connection_params(network="torus")` → `torus`
    - `get_connection_params()` → uses `CLICKHOUSE_DB` env var or `default`

### Removed

- `get_connection_params_from_env()` function removed - use `get_connection_params()` instead

## [0.1.8] - 2025-11-28

### Fixed

- **Jobs celery** (`chainswarm_core.jobs.load_beat_schedule`):
  - Removed DEBUG log when skipping non-dict entries in beat schedule (e.g., `_comment` fields). Non-dict entries are now silently ignored to avoid logs appearing before logger is configured.

## [0.1.7] - 2025-11-28

### Fixed

- **Observability logging** (`chainswarm_core.observability.setup_logger`):
  - Logs directory now correctly resolves to project root by searching for markers (pyproject.toml, requirements.txt, .git, packages) instead of using current working directory which may differ when running scripts with absolute paths

- **Jobs celery** (`chainswarm_core.jobs.load_beat_schedule`):
  - Beat schedule loading no longer logs ERROR when file doesn't exist (this is expected behavior when no schedule is configured)
  - Silently returns empty schedule if file not found
  - Only logs ERROR for actual issues like invalid JSON

## [0.1.6] - 2025-11-28

### Added

- **Observability decorators** (`chainswarm_core.observability`):
  - `log_errors` - Decorator for logging errors with loguru, re-raises exceptions after logging

## [0.1.5] - 2025-11-28

### Added

- **Jobs module** (`chainswarm_core.jobs`):
  - `create_celery_app(name, autodiscover, beat_schedule_path)` - Celery app factory with loguru integration
  - `load_beat_schedule(schedule_path)` - Load beat schedule from JSON with cron string conversion
  - `run_dev_worker(celery_app)` - Run beat + worker in development mode
  - `InterceptHandler` - Redirect stdlib logging to loguru
  - `BaseTask` - Abstract base class for Celery tasks with `@log_errors` decorator
  - `BaseTaskContext` - Base dataclass for task context (network, processing_date, etc.)
  - `BaseTaskResult` - Base dataclass for task results

### Dependencies

- Added `celery[redis]>=5.3.0`

## [0.1.4] - 2025-11-28

### Added

- **Observability module** (`chainswarm_core.observability`):
  - `setup_logger(service_name, logs_dir)` - Loguru setup with JSON file logging and console output
  - `generate_correlation_id()` - Generate unique correlation IDs for request tracing
  - `get_correlation_id()` / `set_correlation_id()` - Thread-local correlation ID storage
  - `terminate_event` - Global threading.Event for graceful shutdown
  - `shutdown_handler(signum, frame)` - Signal handler for SIGINT/SIGTERM
  - `install_shutdown_handlers()` - Register signal handlers (call manually to avoid FastAPI conflicts)
  - `MetricsRegistry` - Prometheus metrics registry with common metrics (health, errors, uptime)
  - `setup_metrics(service_name, port_mapping)` - Setup Prometheus metrics server
  - `get_metrics_registry(service_name)` - Get existing metrics registry
  - `shutdown_metrics_servers()` - Shutdown all metrics servers
  - `manage_metrics(success_metric, failure_metric)` - Decorator for automatic metric recording
  - `DURATION_BUCKETS`, `SIZE_BUCKETS`, `COUNT_BUCKETS` - Standard histogram buckets

### Changed

- Updated `clickhouse-connect` requirement to `>=0.10.0`
- Replaced logging placeholder with full observability module

### Dependencies

- Added `prometheus-client>=0.19.0`
- Added `python-dotenv>=1.0.0`

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