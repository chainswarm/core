"""Network types and blockchain network definitions."""

from enum import Enum


class NetworkType:
    """Classification of blockchain network types."""

    SUBSTRATE = "substrate"
    EVM = "evm"
    UTXO = "utxo"


class Network(Enum):
    """Supported blockchain networks with helper methods."""

    TORUS = "torus"
    TORUS_TESTNET = "torus_testnet"
    TORUS_EVM = "torus_evm"
    TORUS_EVM_TESTNET = "torus_evm_testnet"
    POLKADOT = "polkadot"
    BITTENSOR = "bittensor"
    BITTENSOR_TESTNET = "bittensor_testnet"
    BITTENSOR_EVM = "bittensor_evm"
    BITTENSOR_EVM_TESTNET = "bittensor_evm_testnet"
    BITCOIN = "bitcoin"
    BITCOIN_TESTNET = "bitcoin_testnet"

    @classmethod
    def get_block_time(cls, network: str) -> int:
        """Get the block time in seconds for a network."""
        network = network.lower()
        if network in [
            cls.TORUS.value,
            cls.TORUS_TESTNET.value,
            cls.TORUS_EVM.value,
            cls.TORUS_EVM_TESTNET.value,
        ]:
            return 8
        elif network == cls.POLKADOT.value:
            return 6
        elif network in [
            cls.BITTENSOR.value,
            cls.BITTENSOR_TESTNET.value,
            cls.BITTENSOR_EVM.value,
            cls.BITTENSOR_EVM_TESTNET.value,
        ]:
            return 12
        elif network in [cls.BITCOIN.value, cls.BITCOIN_TESTNET.value]:
            return 600
        raise ValueError(f"Unsupported network: {network}")

    @classmethod
    def get_native_asset_symbol(cls, network: str) -> str:
        """Get the native asset symbol for a network."""
        network = network.lower()
        if network in [
            cls.TORUS.value,
            cls.TORUS_TESTNET.value,
            cls.TORUS_EVM.value,
            cls.TORUS_EVM_TESTNET.value,
        ]:
            return "TOR"
        elif network == cls.POLKADOT.value:
            return "DOT"
        elif network in [
            cls.BITTENSOR.value,
            cls.BITTENSOR_TESTNET.value,
            cls.BITTENSOR_EVM.value,
            cls.BITTENSOR_EVM_TESTNET.value,
        ]:
            return "TAO"
        elif network in [cls.BITCOIN.value, cls.BITCOIN_TESTNET.value]:
            return "BTC"
        raise ValueError(f"Unsupported network: {network}")

    @classmethod
    def get_node_type(cls, network: str) -> str:
        """Get the node type for a network."""
        network = network.lower()
        if network in substrate_networks:
            return "substrate"
        elif network in evm_networks:
            return "evm"
        elif network in utxo_networks:
            return "utxo"
        raise ValueError(f"Unknown network: {network}")


# Network lists by type
substrate_networks = [
    Network.POLKADOT.value,
    Network.TORUS.value,
    Network.TORUS_TESTNET.value,
    Network.BITTENSOR.value,
]

evm_networks = [
    Network.TORUS_EVM.value,
    Network.TORUS_EVM_TESTNET.value,
    Network.BITTENSOR_EVM.value,
    Network.BITTENSOR_EVM_TESTNET.value,
]

utxo_networks = [
    Network.BITCOIN.value,
    Network.BITCOIN_TESTNET.value,
]

networks = substrate_networks + evm_networks + utxo_networks