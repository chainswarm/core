"""Tests for chainswarm_core.constants.addresses module."""

from chainswarm_core.constants.addresses import (
    AddressTypes,
    TrustLevels,
    is_high_risk_address_type,
    is_trusted_address_type,
)


class TestAddressTypes:
    """Tests for AddressTypes class."""

    def test_all_address_types_defined(self):
        """Test that all address types are defined."""
        assert AddressTypes.EXCHANGE == "exchange"
        assert AddressTypes.DEX == "dex"
        assert AddressTypes.MIXER == "mixer"
        assert AddressTypes.DEFI == "defi"
        assert AddressTypes.STAKING == "staking"
        assert AddressTypes.SCAM == "scam"
        assert AddressTypes.INSTITUTIONAL == "institutional"
        assert AddressTypes.WALLET == "wallet"
        assert AddressTypes.BRIDGE == "bridge"
        assert AddressTypes.LENDING == "lending"
        assert AddressTypes.MERCHANT == "merchant"
        assert AddressTypes.GAMBLING == "gambling"
        assert AddressTypes.DARK_MARKET == "dark_market"
        assert AddressTypes.SANCTIONED == "sanctioned"
        assert AddressTypes.UNKNOWN == "unknown"

    def test_blockchain_specific_types(self):
        """Test blockchain-specific address types."""
        assert AddressTypes.VALIDATOR == "validator"
        assert AddressTypes.MINER == "miner"
        assert AddressTypes.AGENT == "agent"
        assert AddressTypes.NEURON == "neuron"
        assert AddressTypes.SUBNET == "subnet"


class TestTrustLevels:
    """Tests for TrustLevels class."""

    def test_all_trust_levels_defined(self):
        """Test that all trust levels are defined."""
        assert TrustLevels.VERIFIED == "verified"
        assert TrustLevels.COMMUNITY == "community"
        assert TrustLevels.UNVERIFIED == "unverified"
        assert TrustLevels.OFFICIAL == "official"
        assert TrustLevels.BLACKLISTED == "blacklisted"


class TestIsHighRiskAddressType:
    """Tests for is_high_risk_address_type function."""

    def test_mixer_is_high_risk(self):
        """Test that mixer is high risk."""
        assert is_high_risk_address_type(AddressTypes.MIXER) is True

    def test_scam_is_high_risk(self):
        """Test that scam is high risk."""
        assert is_high_risk_address_type(AddressTypes.SCAM) is True

    def test_dark_market_is_high_risk(self):
        """Test that dark market is high risk."""
        assert is_high_risk_address_type(AddressTypes.DARK_MARKET) is True

    def test_gambling_is_high_risk(self):
        """Test that gambling is high risk."""
        assert is_high_risk_address_type(AddressTypes.GAMBLING) is True

    def test_sanctioned_is_high_risk(self):
        """Test that sanctioned is high risk."""
        assert is_high_risk_address_type(AddressTypes.SANCTIONED) is True

    def test_exchange_is_not_high_risk(self):
        """Test that exchange is not high risk."""
        assert is_high_risk_address_type(AddressTypes.EXCHANGE) is False

    def test_wallet_is_not_high_risk(self):
        """Test that wallet is not high risk."""
        assert is_high_risk_address_type(AddressTypes.WALLET) is False


class TestIsTrustedAddressType:
    """Tests for is_trusted_address_type function."""

    def test_exchange_is_trusted(self):
        """Test that exchange is trusted."""
        assert is_trusted_address_type(AddressTypes.EXCHANGE) is True

    def test_institutional_is_trusted(self):
        """Test that institutional is trusted."""
        assert is_trusted_address_type(AddressTypes.INSTITUTIONAL) is True

    def test_staking_is_trusted(self):
        """Test that staking is trusted."""
        assert is_trusted_address_type(AddressTypes.STAKING) is True

    def test_validator_is_trusted(self):
        """Test that validator is trusted."""
        assert is_trusted_address_type(AddressTypes.VALIDATOR) is True

    def test_neuron_is_trusted(self):
        """Test that neuron is trusted."""
        assert is_trusted_address_type(AddressTypes.NEURON) is True

    def test_mixer_is_not_trusted(self):
        """Test that mixer is not trusted."""
        assert is_trusted_address_type(AddressTypes.MIXER) is False

    def test_wallet_is_not_trusted(self):
        """Test that wallet is not trusted."""
        assert is_trusted_address_type(AddressTypes.WALLET) is False