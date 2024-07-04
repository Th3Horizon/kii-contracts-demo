"""
Functions that handle connection to the network.
"""

# Standard Library
from typing import Optional
# Third Party
from kiipy.aerial.client import LedgerClient
from kiipy.aerial.config import NetworkConfig, NetworkConfigError, URL_PREFIXES
from web3 import Web3, HTTPProvider
# Package imports
from .common import summarize_exception, log_error, DemoException


# == Core Functions == #
def get_client(
    chain_id: str,
    url: str | None = None,
    fee_denomination: Optional[str] = "tkii",
    staking_denomination: Optional[str] = "tkii",
    fee_minimum_gas_price: Optional[float | int] = 0,
    faucet_url: str | None = None
) -> LedgerClient | None:
    """
    Get a client for the network.

    Parameters
    ----------
    chain_id: str
        The identifier of the chain.
    url: str | none, default = None
        The URL of the network. It should start with one of the following
        prefixes: "grpc+https", "grpc+http", "rest+https", "rest+http".
    fee_denomination: Optional[str], default = 'tkii'
        The denomination of the currency to pay for the fees.
    staking_denomination: Optional[str], default = 'tkii'
        The denomination of the currency to stake.
    fee_minimum_gas_price: Optional[float | int], default = 0
        The minimum gas price to pay for fees.
    faucet_url: str | None, default = None
        The URL of the faucet.

    Returns
    -------
    client: LedgerClient | None
        An instance of the LedgerClient.
        Return None if the network config is invalid.
    """
    try:
        # Retrieve network config
        network_config: NetworkConfig
        if chain_id == "kiiventador":
            network_config = NetworkConfig.kii_testnet()
            network_config.faucet_url = "https://faucet.kiivalidator.com"
        else:
            network_config = NetworkConfig(
                chain_id=chain_id,
                url=url,
                fee_denomination=fee_denomination,
                staking_denomination=staking_denomination,
                fee_minimum_gas_price=fee_minimum_gas_price,
                faucet_url=faucet_url
            )
        # Create client
        client = LedgerClient(
            network_config
        )
        # Return the client
        return client
    except NetworkConfigError as e:
        # Log the error
        log_error(f"Network Error: {e}")
    # Catch all generic exceptions
    except Exception as e:
        # Log the error
        exception_summary = summarize_exception(e)
        log_error(exception_summary)
    # Return default None.
    return None


def get_web3_client(
    network_ref: NetworkConfig | LedgerClient
) -> Web3 | None:
    """
    Get a web3 client for the network.

    Parameters
    ----------
    network_ref: NetworkConfig | LedgerClient
        The network configuration or client.

    Returns
    -------
    web3_client: Web3
        An instance of the Web3 client.
        Return None if the network config is invalid.
    """
    # Retrieve network info.
    if isinstance(
        network_ref,
        NetworkConfig
    ):
        network_config = network_ref
    elif isinstance(
        network_ref,
        LedgerClient
    ):
        network_config = network_ref.network_config
    else:
        raise DemoException(
            "network_ref must be an instance of NetworkConfig or LedgerClient"
        )
    # Parse the info to pass down to the Web3 provider.
    endpoint_uri = network_config.url
    # Check if the prefix is attached.
    if any([
        endpoint_uri.startswith(prefix)
        for prefix in URL_PREFIXES
    ]):
        # Remove the prefix.
        endpoint_uri = endpoint_uri.split("+")[-1]
    # Create the Web3 client.
    try:
        web3_client = Web3(
            HTTPProvider(endpoint_uri)
        )
        # Return the client.
        return web3_client
    except Exception as e:
        # Log the error.
        log_error(
            summarize_exception(e)
        )
    # Default return.
    return None
