"""Tests for chainswarm_core.constants.networks module."""

import pytest

from chainswarm_core.constants.networks import (
    Network,
    NetworkType,
    evm_networks,
    networks,
    substrate_networks,
    utxo_networks,
)


class TestNetworkType:
    """Tests for NetworkType class."""

    def test_network_types_defined(self):
        """Test that all network types are defined."""
        assert NetworkType.SUBSTRATE == "substrate"
        assert NetworkType.EVM == "evm"
        assert NetworkType.UTXO == "utxo"


class TestNetwork:
    """Tests for Network enum."""

    def test_all_networks_defined(self):
        """Test that all networks are defined."""
        assert Network.TORUS.value == "torus"
        assert Network.POLKADOT.value == "polkadot"
        assert Network.BITTENSOR.value == "bittensor"
        assert Network.BITCOIN.value == "bitcoin"

    def test_get_block_time_torus(self):
        """Test block time for Torus networks."""
        assert Network.get_block_time("torus") == 8
        assert Network.get_block_time("torus_testnet") == 8
        assert Network.get_block_time("torus_evm") == 8

    def test_get_block_time_polkadot(self):
        """Test block time for Polkadot."""
        assert Network.get_block_time("polkadot") == 6

    def test_get_block_time_bittensor(self):
        """Test block time for Bittensor networks."""
        assert Network.get_block_time("bittensor") == 12
        assert Network.get_block_time("bittensor_testnet") == 12

    def test_get_block_time_bitcoin(self):
        """Test block time for Bitcoin networks."""
        assert Network.get_block_time("bitcoin") == 600
        assert Network.get_block_time("bitcoin_testnet") == 600

    def test_get_block_time_invalid(self):
        """Test block time raises for invalid network."""
        with pytest.raises(ValueError, match="Unsupported network"):
            Network.get_block_time("invalid_network")

    def test_get_native_asset_symbol_torus(self):
        """Test native asset for Torus."""
        assert Network.get_native_asset_symbol("torus") == "TOR"

    def test_get_native_asset_symbol_polkadot(self):
        """Test native asset for Polkadot."""
        assert Network.get_native_asset_symbol("polkadot") == "DOT"

    def test_get_native_asset_symbol_bittensor(self):
        """Test native asset for Bittensor."""
        assert Network.get_native_asset_symbol("bittensor") == "TAO"

    def test_get_native_asset_symbol_bitcoin(self):
        """Test native asset for Bitcoin."""
        assert Network.get_native_asset_symbol("bitcoin") == "BTC"

    def test_get_native_asset_symbol_invalid(self):
        """Test native asset raises for invalid network."""
        with pytest.raises(ValueError, match="Unsupported network"):
            Network.get_native_asset_symbol("invalid_network")

    def test_get_node_type_substrate(self):
        """Test node type for substrate networks."""
        assert Network.get_node_type("polkadot") == "substrate"
        assert Network.get_node_type("torus") == "substrate"

    def test_get_node_type_evm(self):
        """Test node type for EVM networks."""
        assert Network.get_node_type("torus_evm") == "evm"
        assert Network.get_node_type("bittensor_evm") == "evm"

    def test_get_node_type_utxo(self):
        """Test node type for UTXO networks."""
        assert Network.get_node_type("bitcoin") == "utxo"

    def test_get_node_type_invalid(self):
        """Test node type raises for invalid network."""
        with pytest.raises(ValueError, match="Unknown network"):
            Network.get_node_type("invalid_network")


class TestNetworkLists:
    """Tests for network list constants."""

    def test_substrate_networks_contains_expected(self):
        """Test substrate networks list."""
        assert "polkadot" in substrate_networks
        assert "torus" in substrate_networks
        assert "bittensor" in substrate_networks

    def test_evm_networks_contains_expected(self):
        """Test EVM networks list."""
        assert "torus_evm" in evm_networks
        assert "bittensor_evm" in evm_networks

    def test_utxo_networks_contains_expected(self):
        """Test UTXO networks list."""
        assert "bitcoin" in utxo_networks
        assert "bitcoin_testnet" in utxo_networks

    def test_networks_is_combined(self):
        """Test all networks list is combination."""
        all_networks = substrate_networks + evm_networks + utxo_networks
        assert set(networks) == set(all_networks)