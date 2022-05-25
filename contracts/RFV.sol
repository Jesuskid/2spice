// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract RFV is AccessControl {
    bytes32 public constant ALLOWED_CONTRACTS = keccak256("ALLOWED_CONTRACTS");
    bytes32 public constant DEV_ROLE = keccak256("DEV_ROLE");
    address internal busd;
    event Log(string func, address sender, uint256 value, bytes data);

    constructor(address _busd) {
        busd = _busd;
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    fallback() external payable {
        emit Log("fallback", msg.sender, msg.value, msg.data);
    }

    receive() external payable {
        emit Log("fallback", msg.sender, msg.value, "");
    }

    function transferTo(address rec, uint256 amount)
        public
        onlyRole(ALLOWED_CONTRACTS)
    {
        IERC20(busd).transfer(rec, amount);
    }
}
