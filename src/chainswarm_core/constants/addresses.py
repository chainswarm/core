"""Address types and trust levels for blockchain addresses."""


class AddressTypes:
    """Classification of blockchain address types."""

    EXCHANGE = "exchange"
    DEX = "dex"
    MIXER = "mixer"
    DEFI = "defi"
    STAKING = "staking"
    SCAM = "scam"
    INSTITUTIONAL = "institutional"
    WALLET = "wallet"
    BRIDGE = "bridge"
    LENDING = "lending"
    MERCHANT = "merchant"
    GAMBLING = "gambling"
    DARK_MARKET = "dark_market"
    SANCTIONED = "sanctioned"
    UNKNOWN = "unknown"

    # Blockchain-specific types
    VALIDATOR = "validator"
    MINER = "miner"
    AGENT = "agent"
    NEURON = "neuron"
    SUBNET = "subnet"


class TrustLevels:
    """Trust level classification for addresses."""

    VERIFIED = "verified"
    COMMUNITY = "community"
    UNVERIFIED = "unverified"
    OFFICIAL = "official"
    BLACKLISTED = "blacklisted"


# High risk address types
_HIGH_RISK_ADDRESS_TYPES = {
    AddressTypes.MIXER,
    AddressTypes.SCAM,
    AddressTypes.DARK_MARKET,
    AddressTypes.GAMBLING,
    AddressTypes.SANCTIONED,
}

# Trusted address types
_TRUSTED_ADDRESS_TYPES = {
    AddressTypes.EXCHANGE,
    AddressTypes.INSTITUTIONAL,
    AddressTypes.STAKING,
    AddressTypes.VALIDATOR,
    AddressTypes.NEURON,
}


def is_high_risk_address_type(address_type: str) -> bool:
    """Check if an address type is considered high risk."""
    return address_type in _HIGH_RISK_ADDRESS_TYPES


def is_trusted_address_type(address_type: str) -> bool:
    """Check if an address type is considered trusted."""
    return address_type in _TRUSTED_ADDRESS_TYPES