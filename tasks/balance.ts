// Review the balance from the given token contract deployed at kiichain network.
// NOTE: Currently default to the first available contract address.
// This behaviour will be improved as more contracts are added.

import { task } from "hardhat/config";
import {
    getProviderURL,
    loadJsonFile
} from "../src/utils";

task(
    "balance",
    "Check the balance of an address"
).addParam(
    "address",
    "The address to check the balance of"
).setAction(
    async (taskArgs, hre) => {
        // Initialize the provider
        const provider = new hre.ethers.JsonRpcProvider(
            getProviderURL(hre.network.name)
        );
        // Load the addresses and create the contract instance.
        const tokenAddresses = loadJsonFile("addresses/basictoken.json");
        const basicToken = (
            await hre.ethers.getContractAt(
                "BasicToken",
                tokenAddresses[0]
            )
        ).connect(
            provider
        );
        // Execute the balance check
        const addressToCheck = taskArgs.address;
        const balance = await basicToken.balanceOf(addressToCheck);
        // Log the results
        console.log(
            `Balance of ${addressToCheck}: ${hre.ethers.formatEther(balance)} ETH`
        );
    }
);
