// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Treasury is Ownable {
    address busdAddress = 0x4Fabb145d64652a948d72533023f6E7A623C7C53;
    address earnVilleContract;
    IERC20 busdInterface;

    constructor() {}
}
