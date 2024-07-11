# Kii Contracts Demo

## Description

Demonstrate how to interact with the kiichain (EVM) network using the common ethereum developer kit, for this scenario we are leveraging hardhat.

### Content

- **Contracts**: Contains basic sample smart contracts that can be deployed to the kiichain network.
- **src**: Contains helping typescript functions to handle basic operations like readin a json file or creating an ethers provider instance.
- **tasks**: Contains hardhat tasks that can be executed from the command line to interact with the kiichain network.

### Installation

1. Clone the repository.
2. Run `npm install` to install the dependencies, or any package manager of your preference.
3. Create a `.env` file in the root directory and add the following variables (there should be already an example under the name `.env.sample` for you to copy):
    a. `WALLET_PK`: Private key of the account that will be used to deploy the contracts. It could be a private key from a metamask wallet.
    b. `KIICHAIN_URL`: Public URL of the kiichain network.
4. Run `npx hardhat compile` to compile the contracts.
5. Run one of the available tasks like the deployment routine by using the following command: `npx hardhat deploy --network kiichain` to deploy the contracts to the kiichain network.
