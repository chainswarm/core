/* =========================
   ADDRESS LABELS
   ========================= */

CREATE TABLE IF NOT EXISTS core_address_labels (
    address String,
    network String,
    label String,
    address_type String,          -- exchange, dex, mixer, defi, etc.
    address_subtype String DEFAULT '',
    trust_level String DEFAULT 'unverified',
    source String DEFAULT 'chainswarm',
    metadata String DEFAULT '{}',  -- JSON metadata
    created_at DateTime64(3) DEFAULT now64(3),
    updated_at DateTime64(3) DEFAULT now64(3),
    _version UInt64
)
ENGINE = ReplacingMergeTree(_version)
ORDER BY (network, address)
SETTINGS index_granularity = 8192;

-- Indexes for efficient querying
ALTER TABLE core_address_labels ADD INDEX IF NOT EXISTS idx_address address TYPE bloom_filter(0.01) GRANULARITY 4;
ALTER TABLE core_address_labels ADD INDEX IF NOT EXISTS idx_address_type address_type TYPE bloom_filter(0.01) GRANULARITY 4;
ALTER TABLE core_address_labels ADD INDEX IF NOT EXISTS idx_trust_level trust_level TYPE bloom_filter(0.01) GRANULARITY 4;
ALTER TABLE core_address_labels ADD INDEX IF NOT EXISTS idx_label label TYPE bloom_filter(0.01) GRANULARITY 4;