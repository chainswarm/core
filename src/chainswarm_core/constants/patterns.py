"""Pattern types, detection methods, and pattern roles for analytics."""

from chainswarm_core.constants.risk import RiskLevels


class PatternTypes:
    """
    Pattern types that miners should be able to detect.

    These are the detection targets - each corresponds to one or more
    generators in synthetic pattern generation.
    """

    # Core detection patterns
    CYCLE = "cycle"
    LAYERING_PATH = "layering_path"
    SMURFING_NETWORK = "smurfing_network"
    PROXIMITY_RISK = "proximity_risk"
    MOTIF_FANIN = "motif_fanin"
    MOTIF_FANOUT = "motif_fanout"
    TEMPORAL_BURST = "temporal_burst"
    THRESHOLD_EVASION = "threshold_evasion"

    # Phase 2: High-value additions
    WASH_TRADING = "wash_trading"
    SYBIL_NETWORK = "sybil_network"
    NESTED_SERVICES = "nested_services"

    # Phase 3: Advanced patterns
    RUG_PULL = "rug_pull"
    DORMANT_ACTIVATION = "dormant_activation"


class DetectionMethods:
    """Methods used for pattern detection."""

    SCC_ANALYSIS = "scc_analysis"
    CYCLE_DETECTION = "cycle_detection"
    PATH_ANALYSIS = "path_analysis"
    NETWORK_ANALYSIS = "network_analysis"
    PROXIMITY_ANALYSIS = "proximity_analysis"
    MOTIF_DETECTION = "motif_detection"
    TEMPORAL_ANALYSIS = "temporal_analysis"


# Pattern type to risk level mapping
PATTERN_TYPE_RISK_MAP = {
    # Core patterns
    PatternTypes.CYCLE: RiskLevels.HIGH,
    PatternTypes.LAYERING_PATH: RiskLevels.HIGH,
    PatternTypes.SMURFING_NETWORK: RiskLevels.HIGH,
    PatternTypes.PROXIMITY_RISK: RiskLevels.MEDIUM,
    PatternTypes.MOTIF_FANIN: RiskLevels.MEDIUM,
    PatternTypes.MOTIF_FANOUT: RiskLevels.MEDIUM,
    PatternTypes.TEMPORAL_BURST: RiskLevels.LOW,
    PatternTypes.THRESHOLD_EVASION: RiskLevels.HIGH,
    # Phase 2: High-value additions
    PatternTypes.WASH_TRADING: RiskLevels.HIGH,
    PatternTypes.SYBIL_NETWORK: RiskLevels.MEDIUM,
    PatternTypes.NESTED_SERVICES: RiskLevels.HIGH,
    # Phase 3: Advanced patterns
    PatternTypes.RUG_PULL: RiskLevels.CRITICAL,
    PatternTypes.DORMANT_ACTIVATION: RiskLevels.HIGH,
}


def get_pattern_type_risk_level(pattern_type: str) -> str:
    """Get the risk level for a pattern type."""
    return PATTERN_TYPE_RISK_MAP.get(pattern_type, RiskLevels.MEDIUM)


def is_high_risk_pattern_type(pattern_type: str) -> bool:
    """Check if a pattern type is considered high risk."""
    high_risk_patterns = {
        PatternTypes.CYCLE,
        PatternTypes.LAYERING_PATH,
        PatternTypes.THRESHOLD_EVASION,
        PatternTypes.SMURFING_NETWORK,
        PatternTypes.WASH_TRADING,
        PatternTypes.NESTED_SERVICES,
        PatternTypes.RUG_PULL,
        PatternTypes.DORMANT_ACTIVATION,
    }
    return pattern_type in high_risk_patterns


class PatternRoles:
    """
    Role assignments for addresses in synthetic patterns.

    These are used for ground truth labeling of generated patterns.
    Each generator assigns roles to nodes which are then stored in
    the synthetics_ground_truth table.
    """

    # Existing core roles
    ATTACKER = "attacker"
    ATTACKER_ORIGIN = "attacker_origin"
    MULE = "mule"
    PEEL_DESTINATION = "peel_destination"

    # Mixer roles
    MIXER_CONTRACT = "mixer_contract"
    MIXER_DEPOSITOR = "mixer_depositor"
    MIXER_RECIPIENT = "mixer_recipient"

    # Layering roles
    LAYERING_SOURCE = "layering_source"
    LAYERING_HOP = "layering_hop"
    LAYERING_DEST = "layering_dest"

    # Cycle roles
    CYCLE_NODE = "cycle_node"

    # Centralized service (benign)
    HOT_WALLET = "hot_wallet"
    COLD_WALLET = "cold_wallet"
    DEPOSIT_ADDRESS = "deposit_address"
    WITHDRAWAL_ADDRESS = "withdrawal_address"

    # Phase 1: Smurfing roles
    SMURFING_SOURCE = "smurfing_source"
    SMURFING_MULE = "smurfing_mule"
    SMURFING_INTERMEDIATE = "smurfing_intermediate"
    SMURFING_AGGREGATOR = "smurfing_aggregator"
    SMURFING_EXIT = "smurfing_exit"

    # Phase 1: Threshold evasion roles
    THRESHOLD_SOURCE = "threshold_source"
    THRESHOLD_DESTINATION = "threshold_destination"

    # Phase 1: Fan-in roles
    FANIN_SOURCE = "fanin_source"
    FANIN_COLLECTOR = "fanin_collector"
    FANIN_EXIT = "fanin_exit"

    # Phase 1: Temporal burst roles
    BURST_SOURCE = "burst_source"
    BURST_TARGET = "burst_target"
    BURST_COLLECTOR = "burst_collector"
    BURST_CHAIN_START = "burst_chain_start"
    BURST_CHAIN_HOP = "burst_chain_hop"
    BURST_CHAIN_END = "burst_chain_end"

    # Phase 2: Wash trading roles
    WASH_TRADING_WALLET = "wash_trading_wallet"

    # Phase 2: Sybil network roles
    SYBIL_FUNDER = "sybil_funder"
    SYBIL_WALLET = "sybil_wallet"
    SYBIL_TARGET = "sybil_target"
    SYBIL_COLLECTOR = "sybil_collector"

    # Phase 2: Nested services roles
    NESTED_SERVICE_USER = "nested_service_user"
    NESTED_SERVICE_WALLET = "nested_service_wallet"
    LEGITIMATE_EXCHANGE = "legitimate_exchange"
    NESTED_DESTINATION = "nested_destination"

    # Phase 3: Rug pull roles
    RUG_CONTRACT = "rug_contract"
    RUG_DEVELOPER = "rug_developer"
    RUG_MARKETING = "rug_marketing"
    RUG_VICTIM = "rug_victim"
    RUG_EXIT = "rug_exit"

    # Phase 3: Dormant activation roles
    DORMANT_WALLET = "dormant_wallet"
    ACTIVATION_HOP = "activation_hop"
    DORMANT_EXIT = "dormant_exit"

    # Mutation/noise roles
    NOISE = "noise"
    UNKNOWN = "unknown"


# Role risk categorization
MALICIOUS_ROLES = {
    PatternRoles.ATTACKER,
    PatternRoles.ATTACKER_ORIGIN,
    PatternRoles.MULE,
    PatternRoles.PEEL_DESTINATION,
    PatternRoles.MIXER_CONTRACT,
    PatternRoles.MIXER_DEPOSITOR,
    PatternRoles.MIXER_RECIPIENT,
    PatternRoles.LAYERING_SOURCE,
    PatternRoles.LAYERING_HOP,
    PatternRoles.LAYERING_DEST,
    PatternRoles.CYCLE_NODE,
    PatternRoles.SMURFING_SOURCE,
    PatternRoles.SMURFING_MULE,
    PatternRoles.SMURFING_INTERMEDIATE,
    PatternRoles.SMURFING_AGGREGATOR,
    PatternRoles.SMURFING_EXIT,
    PatternRoles.THRESHOLD_SOURCE,
    PatternRoles.THRESHOLD_DESTINATION,
    PatternRoles.WASH_TRADING_WALLET,
    PatternRoles.SYBIL_FUNDER,
    PatternRoles.SYBIL_WALLET,
    PatternRoles.SYBIL_COLLECTOR,
    PatternRoles.NESTED_SERVICE_WALLET,
    PatternRoles.RUG_DEVELOPER,
    PatternRoles.RUG_CONTRACT,
    PatternRoles.RUG_MARKETING,
    PatternRoles.RUG_EXIT,
    PatternRoles.DORMANT_WALLET,
    PatternRoles.ACTIVATION_HOP,
    PatternRoles.DORMANT_EXIT,
}

VICTIM_ROLES = {
    PatternRoles.PEEL_DESTINATION,
    PatternRoles.RUG_VICTIM,
    PatternRoles.SYBIL_TARGET,
    PatternRoles.NESTED_SERVICE_USER,
}

BENIGN_ROLES = {
    PatternRoles.HOT_WALLET,
    PatternRoles.COLD_WALLET,
    PatternRoles.DEPOSIT_ADDRESS,
    PatternRoles.WITHDRAWAL_ADDRESS,
    PatternRoles.LEGITIMATE_EXCHANGE,
    PatternRoles.NESTED_DESTINATION,
}


def is_malicious_role(role: str) -> bool:
    """Check if a pattern role indicates malicious activity."""
    return role in MALICIOUS_ROLES


def is_victim_role(role: str) -> bool:
    """Check if a pattern role indicates a victim."""
    return role in VICTIM_ROLES


def is_benign_role(role: str) -> bool:
    """Check if a pattern role indicates benign/legitimate activity."""
    return role in BENIGN_ROLES