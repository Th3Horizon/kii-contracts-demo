"""
Dealing with user accounts (wallets)
"""

# Standard Library
from typing import TypeVar
# Third Parties
from kiipy.aerial.client import LedgerClient
from kiipy.aerial.wallet import Wallet, LocalWallet
from kiipy.aerial.faucet import FaucetApi
# Package Imports
from .common import summarize_exception, log_error, DemoException


# == Constants == #
# Generic for any derived wallet class.
WalletType = TypeVar(
    "WalletType",
    bound=Wallet
)


# == Core Functions == #
def get_wallet(
    mode: str = "local",
    create_new: bool = False,
    prefix: str | None = None,
    mnemonic: str | None = None,
    private_key: str | None = None
) -> WalletType | None:
    """
    Get a wallet instance.

    Parameters
    ----------
    mode: str, default = 'local'
        The mode of the wallet. Only 'local' available for now.
    create_new: bool, default = False
        Whether to create a new wallet.
    prefix: str | None, default = None
        The prefix of the wallet. For new wallets.
    mnemonic: str | None, default = None
        The mnemonic of the wallet. For existing wallets.
    private_key: str | None, default = None
        The private key of the wallet. For existing wallets.

    Returns
    -------
    WalletType | None
        An instance of a wallet type. Returns None if any issue arises during
        the process.
    """
    # Check if existing wallet and given parameters are valid.
    if not create_new and not mnemonic and not private_key:
        raise DemoException(
            "Either mnemonic or private key must be provided."
        )
    elif create_new and (mnemonic or private_key):
        raise DemoException(
            "Cannot provide mnemonic or private key for new wallet."
        )
    else:
        try:
            wallet_instance: WalletType
            if create_new:
                match mode:
                    case "local":
                        wallet_instance = LocalWallet.generate(
                            prefix
                        )
                    case _:
                        raise DemoException(
                            f"Invalid mode: {mode}."
                        )
            else:
                match mode:
                    case "local":
                        if mnemonic:
                            wallet_instance = LocalWallet.from_mnemonic(
                                mnemonic,
                                prefix
                            )
                        else:
                            wallet_instance = LocalWallet.from_unsafe_seed(
                                private_key,
                                prefix=prefix
                            )
                    case _:
                        raise DemoException(
                            f"Invalid mode: {mode}."
                        )
            return wallet_instance
        except Exception as e:
            # Log the error.
            log_error(
                summarize_exception(e)
            )
    # Default return.
    return None


def fund_wallet_from_faucet(
    wallet_instance: WalletType,
    network_client:  LedgerClient
) -> None:
    """
    Fund a wallet given a faucet on network client.

    Parameters
    ----------
    wallet_instance: WalletType
        The wallet instance to fund.
    network_client: LedgerClient
        The network client to use for requesting the funding.
    """
    # Check if the wallet is valid.
    if not issubclass(type(wallet_instance), Wallet):
        raise DemoException(
            "Invalid wallet instance."
        )
    else:
        DEFAULT_THRESHOLD = 10 ** 18  # This can be adjusted.
        try:
            # Create a faucet instance.
            faucet = FaucetApi(
                network_client.network_config
            )
            # Check existing balance.
            balance = network_client.query_bank_balance(
                wallet_instance.address()
            )
            # If balance is lower than treshold fund the wallet.
            while balance < DEFAULT_THRESHOLD:
                # Request funds from faucet.
                faucet.get_wealth(
                    wallet_instance.address()
                )
                # Check balance again.
                balance = network_client.query_bank_balance(
                    wallet_instance.address()
                )
        except Exception as e:
            # Log the error.
            log_error(
                summarize_exception(e)
            )
    return None
