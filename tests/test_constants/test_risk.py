"""Tests for chainswarm_core.constants.risk module."""

from chainswarm_core.constants.addresses import AddressTypes
from chainswarm_core.constants.risk import (
    ADDRESS_TYPE_RISK_MAP,
    SUBTYPE_RISK_MODIFIERS,
    AddressSubtypeRiskModifiers,
    RiskLevels,
    Severities,
    get_address_type_risk_level,
    get_subtype_risk_modifier,
)


class TestRiskLevels:
    """Tests for RiskLevels class."""

    def test_all_risk_levels_defined(self):
        """Test that all risk levels are defined."""
        assert RiskLevels.LOW == "low"
        assert RiskLevels.MEDIUM == "medium"
        assert RiskLevels.HIGH == "high"
        assert RiskLevels.CRITICAL == "critical"


class TestSeverities:
    """Tests for Severities class."""

    def test_all_severities_defined(self):
        """Test that all severities are defined."""
        assert Severities.LOW == "low"
        assert Severities.MEDIUM == "medium"
        assert Severities.HIGH == "high"
        assert Severities.CRITICAL == "critical"


class TestAddressTypeRiskMap:
    """Tests for ADDRESS_TYPE_RISK_MAP."""

    def test_low_risk_types(self):
        """Test low risk address types."""
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.EXCHANGE] == RiskLevels.LOW
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.VALIDATOR] == RiskLevels.LOW
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.NEURON] == RiskLevels.LOW

    def test_medium_risk_types(self):
        """Test medium risk address types."""
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.DEFI] == RiskLevels.MEDIUM
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.WALLET] == RiskLevels.MEDIUM
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.UNKNOWN] == RiskLevels.MEDIUM

    def test_high_risk_types(self):
        """Test high risk address types."""
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.GAMBLING] == RiskLevels.HIGH

    def test_critical_risk_types(self):
        """Test critical risk address types."""
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.MIXER] == RiskLevels.CRITICAL
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.SCAM] == RiskLevels.CRITICAL
        assert ADDRESS_TYPE_RISK_MAP[AddressTypes.SANCTIONED] == RiskLevels.CRITICAL


class TestGetAddressTypeRiskLevel:
    """Tests for get_address_type_risk_level function."""

    def test_known_address_type(self):
        """Test getting risk level for known type."""
        assert get_address_type_risk_level(AddressTypes.EXCHANGE) == RiskLevels.LOW
        assert get_address_type_risk_level(AddressTypes.MIXER) == RiskLevels.CRITICAL

    def test_unknown_address_type_returns_medium(self):
        """Test that unknown type returns medium risk."""
        assert get_address_type_risk_level("unknown_type") == RiskLevels.MEDIUM


class TestAddressSubtypeRiskModifiers:
    """Tests for AddressSubtypeRiskModifiers class."""

    def test_well_known_dex_has_lower_risk(self):
        """Test well-known DEXs have lower risk modifiers."""
        assert AddressSubtypeRiskModifiers.UNISWAP_V3 == 0.8
        assert AddressSubtypeRiskModifiers.CURVE == 0.85

    def test_unknown_services_have_higher_risk(self):
        """Test unknown services have higher risk modifiers."""
        assert AddressSubtypeRiskModifiers.UNKNOWN_DEX == 1.2
        assert AddressSubtypeRiskModifiers.UNKNOWN_BRIDGE == 1.3

    def test_exchanges_have_lower_risk(self):
        """Test well-known exchanges have lower risk."""
        assert AddressSubtypeRiskModifiers.BINANCE == 0.8
        assert AddressSubtypeRiskModifiers.COINBASE == 0.8


class TestSubtypeRiskModifiers:
    """Tests for SUBTYPE_RISK_MODIFIERS mapping."""

    def test_dex_modifiers_mapped(self):
        """Test DEX modifiers are in mapping."""
        assert SUBTYPE_RISK_MODIFIERS["uniswap_v3"] == 0.8
        assert SUBTYPE_RISK_MODIFIERS["unknown_dex"] == 1.2

    def test_exchange_modifiers_mapped(self):
        """Test exchange modifiers are in mapping."""
        assert SUBTYPE_RISK_MODIFIERS["binance"] == 0.8


class TestGetSubtypeRiskModifier:
    """Tests for get_subtype_risk_modifier function."""

    def test_known_subtype(self):
        """Test getting modifier for known subtype."""
        assert get_subtype_risk_modifier("uniswap_v3") == 0.8

    def test_unknown_subtype_returns_1(self):
        """Test unknown subtype returns 1.0 (no modification)."""
        assert get_subtype_risk_modifier("unknown_subtype") == 1.0

    def test_none_returns_1(self):
        """Test None returns 1.0 (no modification)."""
        assert get_subtype_risk_modifier(None) == 1.0

    def test_empty_string_returns_1(self):
        """Test empty string returns 1.0 (no modification)."""
        assert get_subtype_risk_modifier("") == 1.0

    def test_case_insensitive(self):
        """Test subtype lookup is case insensitive."""
        assert get_subtype_risk_modifier("UNISWAP_V3") == 0.8
        assert get_subtype_risk_modifier("Binance") == 0.8