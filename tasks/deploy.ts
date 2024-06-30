import { task } from "hardhat/config";
import { getPrivateKey, getProviderURL } from "../src/utils";

task(
    "deploy",
    "Deploy the contract",
    async (_, hre) => {
        const pk = getPrivateKey();
        const provider = new hre.ethers.JsonRpcProvider(
            getProviderURL(hre.network.name)
        );
        const wallet = new hre.ethers.Wallet(
            pk,
            provider
        );

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

        const txReceipt = token.deploymentTransaction();

        console.log(
            `Transaction hash: ${txReceipt?.hash}\n`,
            `Block number: ${txReceipt?.blockNumber}\n`
        );

        console.log(
            `Token Address: ${await token.getAddress()}`
        );
    }
);
