import json
from brownie import (
    accounts,
    config,
    network,
    CoinToken,
    Earnville,
    Insurance,
    Jackpot,
    Treasury,
)
from scripts.helpful_scripts import get_account
from web3 import Web3


def deploy_earnville_and_cointoken(frontend_update=False):
    account = get_account()
    test_address = "0x82CE79a8c5D87E8d73Bc2BF9b943a5fC7b46a65D"
    coin_token = CoinToken.deploy({"from": account})
    insurance = Insurance.deploy(coin_token.address, {"from": account})
    jackpot = Jackpot.deploy(coin_token.address, {"from": account})
    treasury = Treasury.deploy(coin_token.address, {"from": account})
    earnville = Earnville.deploy(
        Web3.toWei(1000000, "ether"),
        jackpot.address,
        insurance.address,
        treasury.address,
        coin_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    busd_amount = Web3.toWei(10000000, "ether")
    xusd_amount = Web3.toWei(1000000, "ether")
    coin_token.approve(earnville.address, busd_amount, {"from": account})
    earnville.approve(earnville.address, xusd_amount, {"from": account})
    tx = earnville.setInitalPoolValue(busd_amount, {"from": account})
    tx.wait(1)
    tx2 = coin_token.transfer(test_address, busd_amount, {"from": account})
    tx.wait(1)
    print("set pool value")

    return earnville, coin_token, insurance, jackpot, treasury


def setPoolPercentages():
    pass


def main():
    deploy_earnville_and_cointoken()
