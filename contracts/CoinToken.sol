// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract CoinToken {
    constructor() ERC20("COIN", "CNT") {
        _mint(msg.sender, 1000000000000000000000000);
    }
}