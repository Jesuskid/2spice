// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Earnville is ERC20, Ownable {
    address busdAddress;

    address jackpotContract;
    address insuranceContract;
    address treasuryContract;

    uint256 liquityPoolValue;
    uint256 jackpotValue;
    uint256 TreasuryValue;

    uint256 APY;

    uint256 xusdAmountInLP;
    uint256 busdAmountInLP;
    mapping(address => uint256) private usersToXusdAmounts;
    address[] buyers;
    address pools;

    //taxes
    //buy
    uint256 public jackpotBuyTax;
    uint256 public TreasuryBuyTax;
    uint256 public LPBuyTax;
    uint256 public insuranceBuyTax;

    //sales
    uint256 jackpotSellTax;
    uint256 TreasurySellTax;
    uint256 LPSellTax;
    uint256 insuranceSellTax;
    bool poolValueSet;

    struct Holder {
        address holder;
        uint256 id;
    }
    address[] private holders;
    mapping(address => Holder) mapping_holders;

    mapping(address => bool) access;

    event Bought(address indexed buyer, uint256 amount);
    event Sold(address indexed seller, uint256 amount);
    event PoolValueSet(address);

    constructor(
        uint256 _initalSupply,
        address _jackPotContract,
        address _insuranceContract,
        address _treasuryContract,
        address _busdAddress
    ) ERC20("Earnville", "EAVL") {
        _mint(msg.sender, _initalSupply);
        jackpotContract = _jackPotContract;
        insuranceContract = _insuranceContract;
        treasuryContract = _treasuryContract;
        busdAddress = _busdAddress;
    }

    modifier isPoolValueSet() {
        require(poolValueSet == true, "pool has not yet been opened");
        _;
    }

    modifier allowRewardControl() {
        require(
            access[msg.sender] == true,
            "You are not allowed to call this contract"
        );
        _;
    }

    function setInitalPoolValue(uint256 busdAmount) public onlyOwner {
        IERC20 busdToken = IERC20(busdAddress);
        IERC20 earnVilleToken = IERC20(address(this));
        uint256 earnvilleAmount = earnVilleToken.balanceOf(msg.sender);
        busdToken.transferFrom(msg.sender, address(this), busdAmount);
        _transfer(msg.sender, address(this), earnvilleAmount);
        poolValueSet = true;
    }

    function buy(uint256 busdAmount) public {
        //transfer the amount bought to the contract address
        IERC20(busdAddress).transferFrom(msg.sender, address(this), busdAmount);

        //get the total busd value held by the contract
        uint256 contractBusdBalance = IERC20(busdAddress).balanceOf(
            address(this)
        );
        uint256 contractXusdBalance = balanceOf(address(this));
        busdAmountInLP = contractBusdBalance;
        xusdAmountInLP = contractXusdBalance;

        //calculates the xusd price
        uint256 xusdPrice = (busdAmountInLP / xusdAmountInLP);

        uint256 jackpotAmount = calculatePercentage(jackpotBuyTax, busdAmount);
        uint256 TreasuryAmount = calculatePercentage(
            TreasuryBuyTax,
            busdAmount
        );
        uint256 InsuranceAmount = calculatePercentage(
            insuranceBuyTax,
            busdAmount
        );
        uint256 LPAmount = calculatePercentage(
            LPBuyTax,
            (busdAmount / xusdPrice)
        ); //xusd addition
        //make transfers to various contract
        transferToPool(jackpotContract, 100);
        transferToPool(treasuryContract, 100);
        transferToPool(insuranceContract, 100);

        //calculates the buying value of busd after taxes
        uint256 purchaseValueBusd = busdAmount -
            (jackpotAmount + TreasuryAmount);

        // The value of XUSD purchased
        uint256 xusdValuePurchased = purchaseValueBusd / xusdPrice;

        //adds user to the array if this is their first purchase
        if (!HolderExist(msg.sender)) {
            mapping_holders[msg.sender] = Holder(msg.sender, holders.length);
            holders.push(msg.sender);
        }

        //updates the amount of xusd held by the contract
        xusdAmountInLP += LPAmount;

        _mint(msg.sender, (xusdValuePurchased - LPAmount));
        _mint(address(this), LPAmount);
        //update amounts
    }

    function sell(uint256 amountInXusd) public {
        uint256 amountHeld = balanceOf(msg.sender);
        //ensures that the balance of token held is equal to the amount
        //required by the msg.sender
        require(amountHeld >= amountHeld);
        uint256 jackpotAmount = calculatePercentage(
            jackpotSellTax,
            amountInXusd
        );
        uint256 TreasuryAmount = calculatePercentage(
            TreasurySellTax,
            amountInXusd
        );
        uint256 LPAmount = calculatePercentage(LPSellTax, amountInXusd);
        uint256 InsuranceAmount = calculatePercentage(
            insuranceSellTax,
            amountInXusd
        );

        //calulate the xusd price
        uint256 xusdPrice = (busdAmountInLP / xusdAmountInLP);

        transferToPool(jackpotContract, (jackpotAmount * xusdPrice));
        transferToPool(treasuryContract, (TreasuryAmount * xusdPrice));
        transferToPool(insuranceContract, (InsuranceAmount * xusdPrice));
        //---------------
        jackpotValue += jackpotAmount;
        TreasuryValue += TreasuryAmount;
        liquityPoolValue += LPAmount;

        uint256 amountAftertaxes = amountInXusd -
            (jackpotAmount + TreasuryAmount + InsuranceAmount + LPAmount);
        uint256 amountTransferableBusd = amountAftertaxes * xusdPrice;
        //transfer bused equivalent to msg.sender
        IERC20(busdAddress).transferFrom(
            address(this),
            msg.sender,
            amountTransferableBusd
        );
        //burns xusd tokens
        burnTokens(amountInXusd, msg.sender);
    }

    //issues rewards to holders of the xusd token from the Treasury to be decided
    function reward() public allowRewardControl {
        for (
            uint256 buyersIndex = 0;
            buyers.length > buyersIndex;
            buyersIndex++
        ) {
            address receipient = buyers[buyersIndex];
            uint256 userTotalValue = balanceOf(receipient);

            if (userTotalValue > 0) {
                uint256 rewardPercentage = calculateAPY30Minutes(
                    userTotalValue
                );
                //send them a token reward based on their total staked value
                _mint(receipient, rewardPercentage);
                IERC20(treasuryContract).transfer(
                    address(this),
                    rewardPercentage
                );
                uint256 xusdPrice = (busdAmountInLP / xusdAmountInLP);
                TreasuryValue -= rewardPercentage / xusdPrice;
            }
        }
    }

    //increases the supply of the xusd tokens given the continues upward price
    function rebase(uint256 _amount) public {
        _mint(address(this), _amount);
        xusdAmountInLP += _amount;
    }

    //Helper functions
    function burnTokens(uint256 amount, address sender) public {
        //burns the tokens by transfering them to address 0
        _transfer(sender, address(0), amount);
    }

    function transferToPool(address _pool, uint256 _amount) public {
        IERC20(busdAddress).transferFrom(address(this), _pool, _amount);
    }

    function calculatePercentage(uint256 _percent, uint256 amount)
        public
        pure
        returns (uint256)
    {
        //require(_percent >= 1, "percentage is less than one");
        require(amount >= 100, "Amount is more than 100");
        return (_percent * amount) / 100;
    }

    function setAPY(uint256 percent) public {
        //divides the expected annual apy to a 30 minute interval
        APY = percent;
    }

    //calculates the APY rewards every 30 minutes
    function calculateAPY30Minutes(uint256 _amountHeldXusd)
        public
        view
        returns (uint256)
    {
        //this function calculates the APY every for 30 minutes
        // 365*48 = 17520
        require(_amountHeldXusd >= 100000);
        uint256 interval = 17520;
        uint256 annualReward = (_amountHeldXusd * APY) / 100;
        uint256 amount = annualReward / interval;
        return amount;
    }

    //check if holder exists
    function HolderExist(address holderAddress) public view returns (bool) {
        if (holders.length == 0) return false;

        return (holders[mapping_holders[holderAddress].id] == holderAddress);
    }

    /** setter functions **/
    //update address

    //update tax amounts

    //buy taxes
    function updateBuyTaxes(
        uint256 _jackpotPercent,
        uint256 _insurancePercent,
        uint256 _treasuryPercent
    ) public {
        require(_jackpotPercent > 0, "");
        jackpotBuyTax = _jackpotPercent;
        insuranceBuyTax = _insurancePercent;
        TreasuryBuyTax = _treasuryPercent;
    }

    //sale taxes
}
