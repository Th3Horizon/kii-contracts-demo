// Deploy one of the available contracts at the kiichain network.
// NOTE: Currently only supports the BasicToken contract.
// It will be improved as more contracts are added.

import { task } from "hardhat/config";
import {
    getPrivateKey, getProviderURL,
    writeJsonFile
} from "../src/utils";

task(
    "deploy",
    "Deploy the contract",
    async (_, hre) => {
        // Initialize the wallet and provider
        const pk = getPrivateKey();
        const provider = new hre.ethers.JsonRpcProvider(
            getProviderURL(hre.network.name)
        );
        const wallet = new hre.ethers.Wallet(
            pk,
            provider
        );
        // Execute the deployment
        console.log("Deploying contracts...\n");
        const tokenFactory = await hre.ethers.getContractFactory(
            "BasicToken",
            wallet
        );
        const token = await tokenFactory.deploy(
            "Test Token",
            "TTest",
            hre.ethers.parseEther("100")
        );
        await token.waitForDeployment();
        // Log the results
        const tokenAddress = await token.getAddress();
        const txReceipt = token.deploymentTransaction();
        const txHash = txReceipt?.hash || "";
        const scannerUrl = "https://app.kiichain.io/kiichain/tx"
        console.log(
            `Token Address: ${tokenAddress}\n`
        );
        if (txHash !== "") {
            console.log(
                `Review the transaction @ ${scannerUrl}/${txHash}`
            )
        };
        // Store the address in a JSON file
        writeJsonFile(
            [tokenAddress],
            "addresses/basictoken.json"
        );
    }
);
