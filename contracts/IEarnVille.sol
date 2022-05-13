// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;

interface IEarnville {
    function buy(uint256 busdAmount) external;

    function sell(uint256 amountInXusd) external;

    function reward() external;
}
