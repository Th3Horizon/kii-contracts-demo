// SPDX-License-Identifier: UNLICENSE

pragma solidity ^0.8.23;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TestToken is ERC20 {
    constructor (
        string memory name,
        string memory symbol
    ) ERC20(name, symbol) {
        _mint(
            msg.sender,
            // Mint 10 ETH worth of tokens
            10 * 10 ** 18
        );
    }
}
