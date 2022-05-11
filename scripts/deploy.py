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
    coin_token = CoinToken.deploy({"from": account})
    insurance = Insurance.deploy({"from": account})
    jackpot = Jackpot.deploy({"from": account})
    treasury = Treasury.deploy({"from": account})
    earnville = Earnville.deploy(
        Web3.toWei(1000000, "ether"),
        jackpot.address,
        treasury.address,
        insurance.address,
        coin_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    return earnville, coin_token, insurance, jackpot, treasury


def main():
    deploy_earnville_and_cointoken()
