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
from scripts.helpful_scripts import get_account, get_contract
from web3 import Web3


def deploy_token_farm_and_dapp(frontend_update=False):
    account = get_account()
    coin_token = CoinToken.deploy({"from": account})
    insurance = Insurance.deploy({"from": account})
    jackpot = Jackpot.deploy({"from": account})
    treasury = Treasury.deploy({"from": account})
    earnville = Earnville.deploy(
        coin_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # tx = dapp_token.transfer(
    #     token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    # )
    # tx.wait(1)

    return earnville, coin_token
