// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract HoldersReward is Ownable {
    address internal busd;
    event Log(string func, address sender, uint256 value, bytes data);

    constructor(address _busd) {
        busd = _busd;
    }

    fallback() external payable {
        emit Log("fallback", msg.sender, msg.value, msg.data);
    }

    receive() external payable {
        emit Log("fallback", msg.sender, msg.value, "");
    }
}
