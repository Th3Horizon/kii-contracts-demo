"""
Module for dealing with contract relating stuff.
"""

# Standard Library
from enum import Enum
import json
import logging
# Third Parties
from solcx import compile_files
from web3 import Web3
from web3.contract import Contract
# Package Imports
from .common import get_root_path, summarize_exception, log_error


# == Constants == #
class ContractType(Enum):
    """
    Enum for the type of contract.
    """
    TestToken = "TestToken"


# == Core Functions == #
def deploy_contract(
    contract_name: ContractType,
    web3_client: Web3
) -> Contract | None:
    """
    Compile a contract, deploy it, and return the instance.

    Parameters
    ----------
    contract_name: ContractType
        The name of any of the available contract.
    web3_client: Web3
        The Web3 client to deploy with.

    Returns
    -------
    contract: Contract | None
        The compiled contract instance already deployed.
        Return None if the contract cannot be compiled.
    """
    try:
        # Get contract path.
        root_path = get_root_path()
        contract_path = root_path / "contracts" / f"{contract_name.value}.sol"
        # Compile contract.
        logging.info(
            f"Compiling contract: {contract_name.value}"
        )
        compiled_contract = compile_files(
            [contract_path],
            output_values=['abi', 'bin'],
            solc_version="0.8.23"
        )
        # Unpack compiled contract.
        _, contract_interface = compiled_contract.popitem()
        bytecode = contract_interface["bin"]
        abi = contract_interface["abi"]
        # Create contract instance.
        contract_factory = web3_client.eth.contract(
            abi=abi,
            bytecode=bytecode
        )
        # Deploy the contract.
        logging.info(
            f"Deploying contract: {contract_name.value}"
        )
        tx_hash = contract_factory.constructor().transact()
        tx_receipt = web3_client.eth.wait_for_transaction_receipt(
            tx_hash
        )
        # Create deployed contract instance.
        contract = web3_client.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )
        # Check if there's existing addresses.
        logging.info(
            f"Storing contract address: {tx_receipt.contractAddress}"
        )
        addresses_path = root_path / "addresses.json"
        try:
            with open(addresses_path, 'r') as f:
                address_dict = json.load(f)
        except FileNotFoundError:
            address_dict = {}
        # Store the address of the contract.
        if not address_dict:
            address_dict = {
                f"{web3_client.eth.chain_id}": {
                    f"{contract_name.value}": f"{tx_receipt.contractAddress}"
                }
            }
        else:
            # Only update if the dictionary with the latest address.
            if (
                web3_client.eth.chain_id not in address_dict
            ):
                # Create a new entry for the chain id and include the contract
                address_dict[
                    str(web3_client.eth.chain_id)
                ][contract_name.value] = tx_receipt.contractAddress
            else:
                # Include/overwrite the contract in the chain id entry.
                address_dict[
                    str(web3_client.eth.chain_id)
                ][contract_name.value] = tx_receipt.contractAddress
        # Store the addresses file with latest changes.
        with open(addresses_path, 'w+') as f:
            json.dump(
                address_dict,
                f,
                indent=4
            )
        # Return compiled contract.
        logging.info(
            f"Contract deployed: {contract_name.value}"
        )
        return contract
    except Exception as e:
        # Log error.
        log_error(
            summarize_exception(e)
        )
    # Return default.
    return None


def get_contract_instance(
    contract_name: ContractType,
    web3_client: Web3
) -> Contract | None:
    """
    Retrieve an existing contract, and return the instance.

    Parameters
    ----------
    contract_name: ContractType
        The name of any of the available contract.
    web3_client: Web3
        The Web3 client to deploy with.

    Returns
    -------
    contract: Contract | None
        The compiled contract instance already deployed.
        Return None if the contract cannot be compiled.
    """
    try:
        # Get contract path.
        root_path = get_root_path()
        # Get the addresses file.
        addresses_path = root_path / "addresses.json"
        try:
            with open(addresses_path, 'r') as f:
                address_dict = json.load(f)
        except FileNotFoundError:
            logging.error(
                "No addresses file found."
            )
            return None
        # Get the contract address.
        contract_address = address_dict[
            str(web3_client.eth.chain_id)
        ][contract_name.value]
        # Get the contract ABI.
        contract_path = root_path / "contracts" / f"{contract_name.value}.sol"
        compiled_contract = compile_files(
            [contract_path],
            output_values=['abi', 'bin'],
            solc_version="0.8.23"
        )
        # Unpack compiled contract.
        _, contract_interface = compiled_contract.popitem()
        abi = contract_interface["abi"]
        # Create contract instance.
        contract = web3_client.eth.contract(
            address=contract_address,
            abi=abi
        )
        # Return compiled contract.
        logging.info(
            f"Contract retrieved: {contract_name.value}"
        )
        return contract
    except Exception as e:
        # Log error.
        log_error(
            summarize_exception(e)
        )
    # Return default.
    return None
