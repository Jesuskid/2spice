// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract Earnville is ERC20, Ownable, ERC20Burnable, ReentrancyGuard {
    address busdAddress;

    address holdersRewardContract;
    address rfvContract;
    address treasuryContract;
    address devContract;

    uint256 public APY;

    uint256 busdAmountInLP;
    mapping(address => uint256) private usersToXusdAmounts;
    address[] public buyers;
    address pools;

    //taxes
    //buy

    uint256 public TreasuryBuyTax = 3;
    uint256 public LPBuyTax = 5;
    uint256 public rfvBuyTax = 5;
    uint256 devBuyTax = 2;

    //sales
    uint256 holdersSellTax = 5;
    uint256 TreasurySellTax = 3;
    uint256 LPSellTax = 5;
    uint256 rfvSellTax = 5;
    uint256 devSellTax = 2;

    bool poolValueSet;
    uint256 public xusdPrice;
    uint256 timeLock;

    struct Holder {
        address holder;
        uint256 id;
    }
    address[] public holders;
    mapping(address => Holder) mapping_holders;

    mapping(address => bool) access;
    mapping(address => uint256) public rewards;

    event Bought(address indexed buyer, uint256 amount);
    event Sold(address indexed seller, uint256 amount);
    event PoolValueSet(address setter);
    event Rewarded(address user, uint256 amount);

    constructor(
        uint256 _initalSupply,
        address _jackPotContract,
        address _insuranceContract,
        address _treasuryContract,
        address _dev,
        address _busdAddress
    ) ERC20("Earnville", "EAVL") {
        _mint(msg.sender, _initalSupply);
        holdersRewardContract = _jackPotContract;
        rfvContract = _insuranceContract;
        treasuryContract = _treasuryContract;
        devContract = _dev;
        busdAddress = _busdAddress;
        timeLock = block.timestamp;
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
        IERC20 earnVilleToken = IERC20(address(this));
        uint256 earnvilleAmount = earnVilleToken.balanceOf(msg.sender);
        require(busdAmount >= earnvilleAmount, "Not enough busd to set value");
        IERC20 busdToken = IERC20(busdAddress);
        busdToken.transferFrom(msg.sender, address(this), busdAmount);
        _transfer(msg.sender, address(this), earnvilleAmount);
        poolValueSet = true;
        emit PoolValueSet(msg.sender);
    }

    function buy(uint256 busdAmount) public isPoolValueSet nonReentrant {
        //transfer the amount bought to the contract address
        IERC20(busdAddress).transferFrom(msg.sender, address(this), busdAmount);

        //calculates the xusd price
        xusdPrice = priceOfXusdInBusd();

        uint256 devAmount = calculatePercentage(
            devBuyTax,
            (busdAmount / xusdPrice)
        );
        uint256 TreasuryAmount = calculatePercentage(
            TreasuryBuyTax,
            busdAmount
        );
        uint256 rfvAmount = calculatePercentage(rfvBuyTax, busdAmount);
        //InsuranceValue = rfvAmount;
        uint256 LPAmount = calculatePercentage(5, busdAmount); //xusd addition
        //make transfers to various contract
        transferToPool(address(this), LPAmount);
        transferToPool(treasuryContract, TreasuryAmount);
        transferToPool(rfvContract, rfvAmount);

        //calculates the buying value of busd after taxes
        uint256 purchaseValueBusd = busdAmount -
            (rfvAmount + TreasuryAmount + devAmount + LPAmount);

        // The value of XUSD purchased
        uint256 xusdValuePurchased = purchaseValueBusd / xusdPrice;

        //adds user to the array if this is their first purchase
        if (!HolderExist(msg.sender)) {
            mapping_holders[msg.sender] = Holder(msg.sender, holders.length);
            holders.push(msg.sender);
        }

        //updates the amount of xusd held by the contract

        _mint(msg.sender, (xusdValuePurchased));
        _mint(devContract, (devAmount / xusdPrice));
        //update amounts
        emit Bought(msg.sender, xusdValuePurchased);
    }

    function sell(uint256 amountInXusd) public isPoolValueSet nonReentrant {
        uint256 amountHeld = IERC20(address(this)).balanceOf(msg.sender);
        //ensures that the balance of token held is equal to the amount
        //required by the msg.sender
        require(amountHeld >= amountInXusd);

        uint256 holdersRewardAmount = calculatePercentage(
            holdersSellTax,
            amountInXusd
        );
        uint256 TreasuryAmount = calculatePercentage(
            TreasurySellTax,
            amountInXusd
        );
        uint256 LPAmount = calculatePercentage(LPSellTax, amountInXusd);
        uint256 rfvAmount = calculatePercentage(rfvSellTax, amountInXusd);

        uint256 devAmount = calculatePercentage(devSellTax, amountInXusd);
        //calulate the xusd price
        uint256 xusdPrice = priceOfXusdInBusd();

        transferToPool(
            holdersRewardContract,
            (holdersRewardAmount * xusdPrice)
        );
        transferToPool(treasuryContract, (TreasuryAmount * xusdPrice));
        transferToPool(rfvContract, (rfvAmount * xusdPrice));
        _transfer(msg.sender, devContract, devAmount);
        //---------------
        uint256 amountAftertaxes = amountInXusd -
            (holdersRewardAmount +
                TreasuryAmount +
                rfvAmount +
                LPAmount +
                devAmount);
        uint256 amountTransferableBusd = amountAftertaxes * xusdPrice;
        //burns seller's xusd tokens
        burn(amountInXusd - devAmount);
        //transfer bused equivalent to msg.sender
        IERC20(busdAddress).transfer(msg.sender, amountTransferableBusd);
        emit Sold(msg.sender, amountInXusd);
    }

    //issues rewards to holders of the xusd token from the Treasury to be decided
    //Not yet tested to ensure it works properly
    function reward() public {
        require(block.timestamp > timeLock, "Cannot issue rewards now");
        for (
            uint256 buyersIndex = 0;
            holders.length > buyersIndex;
            buyersIndex++
        ) {
            address receipient = holders[buyersIndex];
            uint256 userTotalValue = IERC20(address(this)).balanceOf(
                receipient
            );

            if (userTotalValue > 0) {
                uint256 rewardPercentage = calculateAPY30Minutes(
                    userTotalValue
                );
                //send them a token reward based on their total staked value
                rewards[receipient] = rewardPercentage;
            }
        }
        timeLock = block.timestamp + 30 minutes;
    }

    //claim rewards
    function claimReward(address _receipient) external {
        uint256 xusdPrice = priceOfXusdInBusd(); //gets the xusd price
        uint256 rewardAmount = rewards[_receipient]; //sets the reward percentage
        require(rewardAmount >= 100, "Not enouth rewards to claim");
        uint256 rewardBusdToLP = rewardAmount * xusdPrice;
        _mint(_receipient, rewardAmount);
        IERC20(holdersRewardContract).transfer(address(this), rewardBusdToLP);
        emit Rewarded(_receipient, rewardAmount);
    }

    //increases the supply of the xusd tokens given the continues upward price
    function rebase(uint256 _amount) public onlyOwner {
        _mint(address(this), _amount);
    }

    //Helper functions
    function transferToPool(address _pool, uint256 _amount) public {
        IERC20(busdAddress).transfer(_pool, _amount);
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

    function setAPY(uint256 percent) public onlyOwner {
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
        uint256 _rfvPercent,
        uint256 _treasuryPercent,
        uint256 _devPercent,
        uint256 _LPPercent
    ) public onlyOwner {
        require(_rfvPercent > 0, "");
        require(_treasuryPercent > 0, "");
        require(_devPercent > 0, "");
        rfvBuyTax = _rfvPercent;
        TreasuryBuyTax = _treasuryPercent;
        devBuyTax = _devPercent;
        LPBuyTax = _LPPercent;
    }

    //sale taxes
    function updateSellTaxes(
        uint256 _holdersRewardPercent,
        uint256 _rfvPercent,
        uint256 _treasuryPercent,
        uint256 _LPpercent,
        uint256 _devSellTax
    ) public onlyOwner {
        require(_holdersRewardPercent > 0, "");
        require(_rfvPercent > 0, "");
        require(_treasuryPercent > 0, "");
        holdersSellTax = _holdersRewardPercent;
        rfvSellTax = _rfvPercent;
        TreasurySellTax = _treasuryPercent;
        LPSellTax = _LPpercent;
        devSellTax = _devSellTax;
    }

    function priceOfXusdInBusd() public view returns (uint256) {
        uint256 contractBusdBalance = IERC20(busdAddress).balanceOf(
            address(this)
        );
        uint256 contractXusdBalance = IERC20(address(this)).balanceOf(
            address(this)
        );
        return contractBusdBalance / contractXusdBalance;
    }
}
