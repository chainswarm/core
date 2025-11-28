/* =========================
   TRANSFERS
   ========================= */

CREATE TABLE IF NOT EXISTS core_transfers (
    hash String,
    network String,
    block_number UInt64,
    block_timestamp DateTime64(3),
    from_address String,
    to_address String,
    asset_contract String DEFAULT 'native',
    value Decimal128(18),
    fee Decimal128(18) DEFAULT 0,
    success UInt8 DEFAULT 1,
    _version UInt64
)
ENGINE = ReplacingMergeTree(_version)
PARTITION BY toYYYYMM(block_timestamp)
ORDER BY (network, block_timestamp, hash, from_address, to_address, asset_contract)
SETTINGS index_granularity = 8192;

-- Indexes for efficient querying
ALTER TABLE core_transfers ADD INDEX IF NOT EXISTS idx_hash hash TYPE bloom_filter(0.01) GRANULARITY 4;
ALTER TABLE core_transfers ADD INDEX IF NOT EXISTS idx_from_address from_address TYPE bloom_filter(0.01) GRANULARITY 4;
ALTER TABLE core_transfers ADD INDEX IF NOT EXISTS idx_to_address to_address TYPE bloom_filter(0.01) GRANULARITY 4;
ALTER TABLE core_transfers ADD INDEX IF NOT EXISTS idx_asset_contract asset_contract TYPE bloom_filter(0.01) GRANULARITY 4;
ALTER TABLE core_transfers ADD INDEX IF NOT EXISTS idx_block_number block_number TYPE minmax GRANULARITY 4;
ALTER TABLE core_transfers ADD INDEX IF NOT EXISTS idx_block_timestamp block_timestamp TYPE minmax GRANULARITY 4;