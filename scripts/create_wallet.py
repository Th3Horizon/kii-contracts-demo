"""
Creates a new Kii local wallet.
"""

# Standard Library
import json
# Third Party
from kiipy.crypto.address import Address
from kiipy.crypto.keypairs import PrivateKey
from kiipy.aerial.wallet import LocalWallet, Wallet
# Package Imports
from src.network import get_client
from src.accounts import get_wallet, fund_wallet_from_faucet
from src.common import DemoException, get_root_path


# == Runner == #
if __name__ == "__main__":
    try:
        # Create client instance.
        provider = get_client(
            "kiiventador"
        )
        # Create wallet instance.
        wallet_instance: LocalWallet = get_wallet(
            "local",
            create_new=True
        )
        if wallet_instance:
            # Store wallet credentials.
            wallet_address: Address = wallet_instance.address()
            wallet_signer: PrivateKey = wallet_instance.signer()
            wallet_path = f"{get_root_path()}/wallet.json"
            with open(wallet_path, "w") as file:
                json.dump(
                    {
                        "address": wallet_address.data,
                        "private_key": wallet_signer.private_key
                    },
                    file,
                    indent=4
                )
            # Fund wallet.
            fund_wallet_from_faucet(
                wallet_instance,
                provider
            )
    except DemoException as e:
        print(e)
