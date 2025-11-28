"""Tests for chainswarm_core.constants.patterns module."""

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
from chainswarm_core.constants.risk import RiskLevels


class TestPatternTypes:
    """Tests for PatternTypes class."""

    def test_core_patterns_defined(self):
        """Test core pattern types are defined."""
        assert PatternTypes.CYCLE == "cycle"
        assert PatternTypes.LAYERING_PATH == "layering_path"
        assert PatternTypes.SMURFING_NETWORK == "smurfing_network"
        assert PatternTypes.TEMPORAL_BURST == "temporal_burst"
        assert PatternTypes.THRESHOLD_EVASION == "threshold_evasion"

    def test_phase2_patterns_defined(self):
        """Test phase 2 pattern types are defined."""
        assert PatternTypes.WASH_TRADING == "wash_trading"
        assert PatternTypes.SYBIL_NETWORK == "sybil_network"
        assert PatternTypes.NESTED_SERVICES == "nested_services"

    def test_phase3_patterns_defined(self):
        """Test phase 3 pattern types are defined."""
        assert PatternTypes.RUG_PULL == "rug_pull"
        assert PatternTypes.DORMANT_ACTIVATION == "dormant_activation"


class TestDetectionMethods:
    """Tests for DetectionMethods class."""

    def test_all_detection_methods_defined(self):
        """Test all detection methods are defined."""
        assert DetectionMethods.SCC_ANALYSIS == "scc_analysis"
        assert DetectionMethods.CYCLE_DETECTION == "cycle_detection"
        assert DetectionMethods.PATH_ANALYSIS == "path_analysis"
        assert DetectionMethods.NETWORK_ANALYSIS == "network_analysis"
        assert DetectionMethods.PROXIMITY_ANALYSIS == "proximity_analysis"
        assert DetectionMethods.MOTIF_DETECTION == "motif_detection"
        assert DetectionMethods.TEMPORAL_ANALYSIS == "temporal_analysis"


class TestPatternTypeRiskMap:
    """Tests for PATTERN_TYPE_RISK_MAP."""

    def test_high_risk_patterns(self):
        """Test high risk patterns mapping."""
        assert PATTERN_TYPE_RISK_MAP[PatternTypes.CYCLE] == RiskLevels.HIGH
        assert PATTERN_TYPE_RISK_MAP[PatternTypes.LAYERING_PATH] == RiskLevels.HIGH
        assert PATTERN_TYPE_RISK_MAP[PatternTypes.THRESHOLD_EVASION] == RiskLevels.HIGH

    def test_medium_risk_patterns(self):
        """Test medium risk patterns mapping."""
        assert PATTERN_TYPE_RISK_MAP[PatternTypes.PROXIMITY_RISK] == RiskLevels.MEDIUM
        assert PATTERN_TYPE_RISK_MAP[PatternTypes.MOTIF_FANIN] == RiskLevels.MEDIUM

    def test_critical_risk_patterns(self):
        """Test critical risk patterns mapping."""
        assert PATTERN_TYPE_RISK_MAP[PatternTypes.RUG_PULL] == RiskLevels.CRITICAL


class TestGetPatternTypeRiskLevel:
    """Tests for get_pattern_type_risk_level function."""

    def test_known_pattern_type(self):
        """Test getting risk level for known pattern."""
        assert get_pattern_type_risk_level(PatternTypes.CYCLE) == RiskLevels.HIGH

    def test_unknown_pattern_returns_medium(self):
        """Test unknown pattern returns medium risk."""
        assert get_pattern_type_risk_level("unknown_pattern") == RiskLevels.MEDIUM


class TestIsHighRiskPatternType:
    """Tests for is_high_risk_pattern_type function."""

    def test_cycle_is_high_risk(self):
        """Test cycle is high risk."""
        assert is_high_risk_pattern_type(PatternTypes.CYCLE) is True

    def test_layering_is_high_risk(self):
        """Test layering is high risk."""
        assert is_high_risk_pattern_type(PatternTypes.LAYERING_PATH) is True

    def test_rug_pull_is_high_risk(self):
        """Test rug pull is high risk."""
        assert is_high_risk_pattern_type(PatternTypes.RUG_PULL) is True

    def test_temporal_burst_is_not_high_risk(self):
        """Test temporal burst is not high risk."""
        assert is_high_risk_pattern_type(PatternTypes.TEMPORAL_BURST) is False


class TestPatternRoles:
    """Tests for PatternRoles class."""

    def test_core_roles_defined(self):
        """Test core pattern roles are defined."""
        assert PatternRoles.ATTACKER == "attacker"
        assert PatternRoles.MULE == "mule"
        assert PatternRoles.CYCLE_NODE == "cycle_node"

    def test_benign_roles_defined(self):
        """Test benign roles are defined."""
        assert PatternRoles.HOT_WALLET == "hot_wallet"
        assert PatternRoles.COLD_WALLET == "cold_wallet"
        assert PatternRoles.DEPOSIT_ADDRESS == "deposit_address"


class TestRoleSets:
    """Tests for role categorization sets."""

    def test_malicious_roles_contains_expected(self):
        """Test MALICIOUS_ROLES contains expected roles."""
        assert PatternRoles.ATTACKER in MALICIOUS_ROLES
        assert PatternRoles.MIXER_CONTRACT in MALICIOUS_ROLES
        assert PatternRoles.RUG_DEVELOPER in MALICIOUS_ROLES

    def test_victim_roles_contains_expected(self):
        """Test VICTIM_ROLES contains expected roles."""
        assert PatternRoles.RUG_VICTIM in VICTIM_ROLES
        assert PatternRoles.SYBIL_TARGET in VICTIM_ROLES

    def test_benign_roles_contains_expected(self):
        """Test BENIGN_ROLES contains expected roles."""
        assert PatternRoles.HOT_WALLET in BENIGN_ROLES
        assert PatternRoles.LEGITIMATE_EXCHANGE in BENIGN_ROLES


class TestIsMaliciousRole:
    """Tests for is_malicious_role function."""

    def test_attacker_is_malicious(self):
        """Test attacker is malicious."""
        assert is_malicious_role(PatternRoles.ATTACKER) is True

    def test_hot_wallet_is_not_malicious(self):
        """Test hot wallet is not malicious."""
        assert is_malicious_role(PatternRoles.HOT_WALLET) is False


class TestIsVictimRole:
    """Tests for is_victim_role function."""

    def test_rug_victim_is_victim(self):
        """Test rug victim is victim."""
        assert is_victim_role(PatternRoles.RUG_VICTIM) is True

    def test_attacker_is_not_victim(self):
        """Test attacker is not victim."""
        assert is_victim_role(PatternRoles.ATTACKER) is False


class TestIsBenignRole:
    """Tests for is_benign_role function."""

    def test_hot_wallet_is_benign(self):
        """Test hot wallet is benign."""
        assert is_benign_role(PatternRoles.HOT_WALLET) is True

    def test_attacker_is_not_benign(self):
        """Test attacker is not benign."""
        assert is_benign_role(PatternRoles.ATTACKER) is False