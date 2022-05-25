// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

interface ISpice {
    function sell(uint256 amountInXusd) external;
}

contract Dev is AccessControl {
    bytes32 public constant ALLOWED_CONTRACTS = keccak256("ALLOWED_CONTRACTS");
    bytes32 public constant DEV_ROLE = keccak256("DEV_ROLE");

    address internal spice;
    address busd;
    event Log(string func, address sender, uint256 value, bytes data);

    constructor(address _admin, address _busd) {
        _setupRole(DEV_ROLE, msg.sender);
        _setupRole(DEFAULT_ADMIN_ROLE, _admin);
        busd = _busd;
    }

    function setSpice(address _spiceContract) public onlyRole(DEV_ROLE) {
        spice = _spiceContract;
    }

    fallback() external payable {
        emit Log("fallback", msg.sender, msg.value, msg.data);
    }

    receive() external payable {
        emit Log("fallback", msg.sender, msg.value, "");
    }

    function sellSpice(address rec, uint256 amount)
        public
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        ISpice(spice).sell(amount);
    }

    function transferTo(address rec, uint256 amount)
        public
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        uint256 balance = IERC20(busd).balanceOf(address(this));
        IERC20(busd).transfer(rec, amount);
    }
}
