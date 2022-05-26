# objectives
# =========================================================
import web3
from scripts.deploy import deploy_earnville_and_cointoken
from scripts.helpful_scripts import get_account
from web3 import Web3

# deploy mocktoken

# deploy pool contracts
# deploy earnville
# test pool contract address setting
def test_deploy_mock_token():
    # Arrange
    account = get_account()
    (
        earnville,
        coin_token,
        rfv,
        holders_reward,
        treasury,
        dev,
    ) = deploy_earnville_and_cointoken()

    # ACT

    # Assert
    assert coin_token.balanceOf(account) >= Web3.toWei(1000000, "ether")
    assert coin_token.balanceOf(rfv.address) == Web3.toWei(0, "ether")
    assert coin_token.balanceOf(holders_reward.address) == Web3.toWei(0, "ether")
    assert coin_token.balanceOf(treasury.address) == Web3.toWei(0, "ether")
    assert coin_token.balanceOf(dev.address) == Web3.toWei(0, "ether")


# test set inital pool value
def test_setInitial_poolValue():
    # Arrange
    account = get_account()
    (
        earnville,
        coin_token,
        rfv,
        holders_reward,
        treasury,
        dev,
    ) = deploy_earnville_and_cointoken()

    # act
    busd_amount = Web3.toWei(10000000, "ether")
    # xusd_amount = Web3.toWei(1000000, "ether")
    # coin_token.approve(earnville.address, busd_amount, {"from": account})
    # earnville.approve(earnville.address, xusd_amount, {"from": account})
    # tx = earnville.setInitalPoolValue(busd_amount, {"from": account})
    # tx.wait(1)

    # assert
    assert coin_token.balanceOf(earnville.address) == busd_amount
    assert earnville.balanceOf(account) == 0


# test update fees


# test buying
def test_buying_operation():
    # Arrange
    account = get_account()
    (
        earnville,
        coin_token,
        rfv,
        holders_reward,
        treasury,
        dev,
    ) = deploy_earnville_and_cointoken()
    # Act
    infinit_busd_amount = Web3.toWei(
        1000000000000000000000000000000000000000000000000000, "ether"
    )
    set_busd_amount = Web3.toWei(10000000, "ether")
    busd_amount = Web3.toWei(1000, "ether")
    xusd_amount = Web3.toWei(100, "ether")
    earnvilleBusdBalanceBeforePurchase = coin_token.balanceOf(earnville.address)
    ##set approvals
    print(coin_token.balanceOf(rfv.address))
    # set initial pool values
    coin_token.approve(earnville.address, infinit_busd_amount, {"from": account})
    earnville.approve(earnville.address, infinit_busd_amount, {"from": account})
    # tx = earnville.setInitalPoolValue(set_busd_amount, {"from": account})
    # tx.wait(1)
    ## set taxes percentage
    tx1b = earnville.updateBuyTaxes(5, 3, 10, 5, {"from": account})
    tx1b.wait(1)
    ##
    coin_token.approve(earnville.address, busd_amount, {"from": account})
    tx2 = earnville.buy(busd_amount)
    tx2.wait(1)
    print(coin_token.balanceOf(rfv.address))
    # assert-------------------------------------------------------------------
    # buying fees percentages are ok
    assert earnville.rfvBuyTax() == 5
    print("passed the set buy taxes")
    # tokens where minted to msg.sender
    assert earnville.balanceOf(account) > 0
    # balance of contracts has increased
    # assert coin_token.balanceOf(
    #     earnville.address
    # ) == earnvilleBusdBalanceBeforePurchase + Web3.toWei(
    #     busd_amount, "ether"
    # ) + Web3.toWei(
    #     busd_amount, "ether"
    # )
    # Test that the buying fees collected are correct
    j_percentage = earnville.calculatePercentage(5, busd_amount)
    i_percentage = earnville.calculatePercentage(3, busd_amount)
    t_percentage = earnville.calculatePercentage(10, busd_amount)
    assert earnville.balanceOf(earnville.address) > 0
    assert coin_token.balanceOf(rfv.address) == j_percentage
    assert coin_token.balanceOf(treasury.address) == i_percentage
    assert earnville.balanceOf(dev.address) > 0


# test buying fees collection
def test_holding_rewards():
    # Arrange
    account = get_account()
    (
        earnville,
        coin_token,
        rfv,
        holders_reward,
        treasury,
        dev,
    ) = deploy_earnville_and_cointoken()
    infinit_busd_amount = Web3.toWei(
        1000000000000000000000000000000000000000000000000000, "ether"
    )
    set_busd_amount = Web3.toWei(10000000, "ether")
    busd_amount = Web3.toWei(1000, "ether")
    xusd_amount = Web3.toWei(100, "ether")
    xusd_sell_amount = Web3.toWei(10, "ether")
    earnvilleBusdBalanceBeforePurchase = coin_token.balanceOf(earnville.address)
    ##set approvals
    coin_token.approve(earnville.address, infinit_busd_amount, {"from": account})
    earnville.approve(earnville.address, infinit_busd_amount, {"from": account})
    ## set taxes percentage
    coin_token.approve(earnville.address, busd_amount, {"from": account})
    tx2 = earnville.buy(busd_amount)
    tx2.wait(1)
    ###ACT
    tx2 = earnville.setAPY(99)
    tx2.wait(1)

    tx3 = coin_token.approve(earnville.address, infinit_busd_amount, {"from": account})
    tx3.wait(1)
    sellTx = earnville.sell(xusd_sell_amount, {"from": account})
    sellTx.wait(1)
    balance_before = earnville.balanceOf(account)
    print(f"holders balance: {coin_token.balanceOf(holders_reward.address)}")
    print(earnville.holders(0))
    print(balance_before)
    print(earnville.balanceOf(account))
    print(earnville.calculateAPY30Minutes(earnville.balanceOf(account)))
    tx = earnville.reward()
    tx.wait(1)
    print(earnville.rewards(account))
    print(earnville.balanceOf(account))

    ##assert
    assert earnville.balanceOf(account) > balance_before
    assert earnville.rewards(account) == 0


# test selling
def test_selling():
    # Arrange
    account = get_account()
    (
        earnville,
        coin_token,
        rfv,
        holders_reward,
        treasury,
        dev,
    ) = deploy_earnville_and_cointoken()
    infinit_busd_amount = Web3.toWei(
        1000000000000000000000000000000000000000000000000000, "ether"
    )
    set_busd_amount = Web3.toWei(10000000, "ether")
    busd_amount = Web3.toWei(1000, "ether")
    xusd_amount = Web3.toWei(100, "ether")
    earnvilleBusdBalanceBeforePurchase = coin_token.balanceOf(earnville.address)
    ##set approvals
    coin_token.approve(earnville.address, infinit_busd_amount, {"from": account})
    earnville.approve(earnville.address, infinit_busd_amount, {"from": account})
    ## set taxes percentage
    tx1c = earnville.updateBuyTaxes(5, 3, 10, 5, {"from": account})
    tx1c.wait(1)
    tx1b = earnville.updateSellTaxes(5, 3, 10, 5, 2, {"from": account})
    tx1b.wait(1)
    ##
    coin_token.approve(earnville.address, busd_amount, {"from": account})
    tx2 = earnville.buy(busd_amount)
    tx2.wait(1)

    j_value = coin_token.balanceOf(holders_reward.address)
    i_value = coin_token.balanceOf(rfv.address)
    t_value = coin_token.balanceOf(treasury.address)
    print(j_value)

    # Act -----------------------------------------------
    closing_balance = earnville.balanceOf(account)
    total_supply = earnville.totalSupply()
    xusd_sell_amount = Web3.toWei(10, "ether")
    sellTx = earnville.sell(xusd_sell_amount, {"from": account})
    sellTx.wait(1)

    ##check sell fees are collected and correct
    j_percentage = earnville.calculatePercentage(5, xusd_sell_amount)
    i_percentage = earnville.calculatePercentage(3, xusd_sell_amount)
    t_percentage = earnville.calculatePercentage(10, xusd_sell_amount)
    d_percentage = earnville.calculatePercentage(2, xusd_sell_amount)

    ##assert

    # assert coin_token.balanceOf(holders_reward.address) > j_value
    # assert coin_token.balanceOf(rfv.address) > i_value
    # assert coin_token.balanceOf(treasury.address) > t_value
    print(earnville.totalSupply() - (total_supply - (xusd_sell_amount - d_percentage)))
    ##check tokens are burnt
    assert earnville.balanceOf(account) == closing_balance - xusd_sell_amount
    assert earnville.totalSupply() == (total_supply - (xusd_sell_amount - d_percentage))


# test rewards
