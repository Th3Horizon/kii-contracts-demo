import "@nomicfoundation/hardhat-ethers";
import "@nomicfoundation/hardhat-chai-matchers";
import "@typechain/hardhat";
import dotenv from "dotenv";
import type { HardhatUserConfig } from "hardhat/config";

import "./tasks";

dotenv.config();

const config: HardhatUserConfig = {
    defaultNetwork: "hardhat",
    networks: {
        hardhat: {
            accounts: {}
        },
        kiichain: {
            url: `${process.env.KIICHAIN_URL}`,
            chainId: 123454321,
            accounts: [process.env.WALLET_PK || ""]
        }
    },
    paths: {
        artifacts: "./artifacts",
        cache: "./cache",
        sources: "./contracts",
        tests: "./tests",
    },
    typechain: {
        outDir: "./typechain",
        target: "ethers-v6",
    },
    solidity: { 
        compilers: [
            {
                version: "0.8.26",
                settings: {
                    optimizer: {
                        enabled: true,
                        runs: 500
                    }
                }
            }
        ]
    }
};

export default config;

