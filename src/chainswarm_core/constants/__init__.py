"""Constants for blockchain networks, address types, risk levels, and patterns."""

from chainswarm_core.constants.addresses import (
    AddressTypes,
    TrustLevels,
    is_high_risk_address_type,
    is_trusted_address_type,
)
from chainswarm_core.constants.networks import (
    Network,
    NetworkType,
    evm_networks,
    networks,
    substrate_networks,
    utxo_networks,
)
from chainswarm_core.constants.patterns import (
    BENIGN_ROLES,
    MALICIOUS_ROLES,
    PATTERN_TYPE_RISK_MAP,
    VICTIM_ROLES,
    DetectionMethods,
    PatternRoles,
    PatternTypes,
    get_pattern_type_risk_level,
    is_benign_role,
    is_high_risk_pattern_type,
    is_malicious_role,
    is_victim_role,
)
from chainswarm_core.constants.risk import (
    ADDRESS_TYPE_RISK_MAP,
    SUBTYPE_RISK_MODIFIERS,
    AddressSubtypeRiskModifiers,
    RiskLevels,
    Severities,
    get_address_type_risk_level,
    get_subtype_risk_modifier,
)

__all__ = [
    # Networks
    "NetworkType",
    "Network",
    "substrate_networks",
    "evm_networks",
    "utxo_networks",
    "networks",
    # Addresses
    "AddressTypes",
    "TrustLevels",
    "is_high_risk_address_type",
    "is_trusted_address_type",
    # Risk
    "RiskLevels",
    "Severities",
    "ADDRESS_TYPE_RISK_MAP",
    "AddressSubtypeRiskModifiers",
    "SUBTYPE_RISK_MODIFIERS",
    "get_address_type_risk_level",
    "get_subtype_risk_modifier",
    # Patterns
    "PatternTypes",
    "DetectionMethods",
    "PatternRoles",
    "PATTERN_TYPE_RISK_MAP",
    "MALICIOUS_ROLES",
    "VICTIM_ROLES",
    "BENIGN_ROLES",
    "get_pattern_type_risk_level",
    "is_high_risk_pattern_type",
    "is_malicious_role",
    "is_victim_role",
    "is_benign_role",
]