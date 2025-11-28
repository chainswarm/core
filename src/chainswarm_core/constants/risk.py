"""Risk levels, severities, and risk mappings."""

from chainswarm_core.constants.addresses import AddressTypes


class RiskLevels:
    """Risk level classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Severities:
    """Severity level classification (alias for RiskLevels in alert contexts)."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Mapping of address types to their default risk levels
ADDRESS_TYPE_RISK_MAP = {
    # Low risk
    AddressTypes.EXCHANGE: RiskLevels.LOW,
    AddressTypes.DEX: RiskLevels.LOW,
    AddressTypes.INSTITUTIONAL: RiskLevels.LOW,
    AddressTypes.STAKING: RiskLevels.LOW,
    AddressTypes.VALIDATOR: RiskLevels.LOW,
    AddressTypes.MINER: RiskLevels.LOW,
    AddressTypes.NEURON: RiskLevels.LOW,
    AddressTypes.SUBNET: RiskLevels.LOW,
    # Medium risk
    AddressTypes.DEFI: RiskLevels.MEDIUM,
    AddressTypes.LENDING: RiskLevels.MEDIUM,
    AddressTypes.AGENT: RiskLevels.MEDIUM,
    AddressTypes.BRIDGE: RiskLevels.MEDIUM,
    AddressTypes.MERCHANT: RiskLevels.MEDIUM,
    AddressTypes.WALLET: RiskLevels.MEDIUM,
    AddressTypes.UNKNOWN: RiskLevels.MEDIUM,
    # High risk
    AddressTypes.GAMBLING: RiskLevels.HIGH,
    # Critical risk
    AddressTypes.MIXER: RiskLevels.CRITICAL,
    AddressTypes.SCAM: RiskLevels.CRITICAL,
    AddressTypes.DARK_MARKET: RiskLevels.CRITICAL,
    AddressTypes.SANCTIONED: RiskLevels.CRITICAL,
}


def get_address_type_risk_level(address_type: str) -> str:
    """Get the risk level for an address type."""
    return ADDRESS_TYPE_RISK_MAP.get(address_type, RiskLevels.MEDIUM)


class AddressSubtypeRiskModifiers:
    """
    Risk modifiers for specific address subtypes.

    Applied as multipliers to base address_type risk score.
    Range: 0.8 (reduce risk 20%) to 1.3 (increase risk 30%)
    """

    # Bittensor subnet modifiers
    SUBNET_1 = 1.0  # Main subnet
    SUBNET_18 = 1.0  # Standard subnet
    SUBNET_UNKNOWN = 1.1  # Unknown subnet slightly higher risk

    # DEX modifiers (EVM)
    UNISWAP_V3 = 0.8  # Well-established, lower risk
    UNISWAP_V2 = 0.85
    SUSHISWAP = 0.9
    PANCAKESWAP = 0.9
    CURVE = 0.85
    BALANCER = 0.9
    UNKNOWN_DEX = 1.2  # Unknown DEX higher risk

    # Bridge modifiers
    WORMHOLE = 1.0
    STARGATE = 1.0
    LAYERZERO = 1.0
    ACROSS = 1.0
    HOP = 1.0
    UNKNOWN_BRIDGE = 1.3  # Unknown bridge higher risk

    # Lending protocol modifiers
    AAVE = 0.8
    COMPOUND = 0.8
    MAKER = 0.8
    UNKNOWN_LENDING = 1.2

    # Exchange modifiers
    BINANCE = 0.8
    COINBASE = 0.8
    KRAKEN = 0.8
    UNKNOWN_EXCHANGE = 1.1

    # AI Agent modifiers (Torus/Bittensor)
    TRADING_BOT = 1.1
    ORACLE_AGENT = 1.0
    UNKNOWN_AGENT = 1.2


# Subtype risk modifier mapping
SUBTYPE_RISK_MODIFIERS = {
    # Bittensor
    "subnet_1": AddressSubtypeRiskModifiers.SUBNET_1,
    "subnet_18": AddressSubtypeRiskModifiers.SUBNET_18,
    "subnet_unknown": AddressSubtypeRiskModifiers.SUBNET_UNKNOWN,
    # DEXs
    "uniswap_v3": AddressSubtypeRiskModifiers.UNISWAP_V3,
    "uniswap_v2": AddressSubtypeRiskModifiers.UNISWAP_V2,
    "sushiswap": AddressSubtypeRiskModifiers.SUSHISWAP,
    "pancakeswap": AddressSubtypeRiskModifiers.PANCAKESWAP,
    "curve": AddressSubtypeRiskModifiers.CURVE,
    "balancer": AddressSubtypeRiskModifiers.BALANCER,
    "unknown_dex": AddressSubtypeRiskModifiers.UNKNOWN_DEX,
    # Bridges
    "wormhole": AddressSubtypeRiskModifiers.WORMHOLE,
    "stargate": AddressSubtypeRiskModifiers.STARGATE,
    "layerzero": AddressSubtypeRiskModifiers.LAYERZERO,
    "across": AddressSubtypeRiskModifiers.ACROSS,
    "hop": AddressSubtypeRiskModifiers.HOP,
    "unknown_bridge": AddressSubtypeRiskModifiers.UNKNOWN_BRIDGE,
    # Lending
    "aave": AddressSubtypeRiskModifiers.AAVE,
    "compound": AddressSubtypeRiskModifiers.COMPOUND,
    "maker": AddressSubtypeRiskModifiers.MAKER,
    "unknown_lending": AddressSubtypeRiskModifiers.UNKNOWN_LENDING,
    # Exchanges
    "binance": AddressSubtypeRiskModifiers.BINANCE,
    "coinbase": AddressSubtypeRiskModifiers.COINBASE,
    "kraken": AddressSubtypeRiskModifiers.KRAKEN,
    "unknown_exchange": AddressSubtypeRiskModifiers.UNKNOWN_EXCHANGE,
    # AI Agents
    "trading_bot": AddressSubtypeRiskModifiers.TRADING_BOT,
    "oracle_agent": AddressSubtypeRiskModifiers.ORACLE_AGENT,
    "unknown_agent": AddressSubtypeRiskModifiers.UNKNOWN_AGENT,
}


def get_subtype_risk_modifier(address_subtype: str) -> float:
    """
    Get risk modifier for address subtype.

    Returns 1.0 if subtype not found (no modification).
    """
    if not address_subtype:
        return 1.0
    return SUBTYPE_RISK_MODIFIERS.get(address_subtype.lower(), 1.0)