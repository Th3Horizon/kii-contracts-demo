// Utilities related with objects and instances to interact with an EVM network.

import { isHexString, SigningKey } from "ethers";

/**
 * Gets the Private Key from the `.env` file.
 * 
 * @returns A SigningKey instance with the PK provided.
 */
export function getPrivateKey() {
    require("dotenv").config();
    const inputKey = process.env['WALLET_PK'] 
        ? process.env['WALLET_PK'] : null;
    let privateKey;
    if (inputKey) {
        privateKey = isHexString(inputKey) ? inputKey : "0x" + inputKey;
        return new SigningKey(privateKey);
    }
    else {
        throw Error(`Theres no Private Key available`)
    }
};

/*
 * Returns the provider URL from `.env` file.
 * 
 * @param network The name of network to get the provider url from.
 * 
 * @returns The URL for the indicated provider.
*/
export function getProviderURL(
    network: string
) {
    require("dotenv").config();
    return process.env[`${network.toUpperCase()}_URL`] || "";
}
