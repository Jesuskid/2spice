# objectives
# =========================================================
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
        insurance,
        jackpot,
        treasury,
    ) = deploy_earnville_and_cointoken()

    # ACT

    # Assert
    assert coin_token.balanceOf(account) >= Web3.toWei(1000000, "ether")
    assert coin_token.balanceOf(insurance.address) == Web3.toWei(0, "ether")
    assert coin_token.balanceOf(jackpot.address) == Web3.toWei(0, "ether")
    assert coin_token.balanceOf(treasury.address) == Web3.toWei(0, "ether")


# test set inital pool value
def test_setInitial_poolValue():
    # Arrange
    account = get_account()
    (
        earnville,
        coin_token,
        insurance,
        jackpot,
        treasury,
    ) = deploy_earnville_and_cointoken()

    # act
    busd_amount = Web3.toWei(10000000, "ether")
    xusd_amount = Web3.toWei(1000000, "ether")
    coin_token.approve(earnville.address, busd_amount, {"from": account})
    earnville.approve(earnville.address, xusd_amount, {"from": account})
    tx = earnville.setInitalPoolValue(busd_amount, {"from": account})
    tx.wait(1)

    assert coin_token.balanceOf(earnville.address) == busd_amount


# test buying
# def test_buying_operation():
#     # Arrange
#     account = get_account()
#     (
#         earnville,
#         coin_token,
#         insurance,
#         jackpot,
#         treasury,
#     ) = deploy_earnville_and_cointoken()
#     # Act
#     busd_amount = Web3.toWei(10000000, "ether")
#     tx = earnville.setInitalPoolValue(busd_amount, {"from": account})
#     tx.wait()
#     coin_token.approve(earnville.address, busd_amount, {"from": account})
#     tx2 = earnville.buy(busd_amount, {"from": account})
#     tx2.wait()


# test buying fees collection
# test selling
# test selling fees collection
