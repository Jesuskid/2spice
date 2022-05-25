import json
from brownie import (
    accounts,
    config,
    network,
    CoinToken,
    Spice,
    Dev,
    HoldersReward,
    RFV,
    Treasury,
)
from scripts.helpful_scripts import get_account
from web3 import Web3


def deploy_earnville_and_cointoken(frontend_update=False):
    account = get_account()
    test_address = "0x82CE79a8c5D87E8d73Bc2BF9b943a5fC7b46a65D"
    coin_token = CoinToken.deploy({"from": account})
    rfv = RFV.deploy(coin_token.address, {"from": account})
    holders_reward = HoldersReward.deploy(coin_token.address, {"from": account})
    treasury = Treasury.deploy(coin_token.address, {"from": account})
    dev = Dev.deploy(account, coin_token.address, {"from": account})
    earnville = Spice.deploy(
        Web3.toWei(1000000, "ether"),
        holders_reward.address,
        rfv.address,
        treasury.address,
        dev.address,
        coin_token.address,
        account,
        99,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    busd_amount = Web3.toWei(10000000, "ether")
    xusd_amount = Web3.toWei(1000000, "ether")
    coin_token.approve(earnville.address, busd_amount, {"from": account})
    earnville.approve(earnville.address, xusd_amount, {"from": account})
    tx = earnville.setInitalPoolValue(busd_amount, {"from": account})
    tx.wait(1)
    coin_token.approve(holders_reward.address, busd_amount, {"from": account})
    # tx2 = coin_token.transferFrom(
    #     account, holders_reward.address, busd_amount, {"from": account}
    # )
    # tx2.wait(1)
    print("set pool value")
    allow_contract_h = holders_reward.ALLOWED_CONTRACTS()
    default_admin = holders_reward.DEFAULT_ADMIN_ROLE()

    tx_h = holders_reward.grantRole(
        allow_contract_h, earnville.address, {"from": account}
    )
    tx_h.wait(1)
    tx_r = rfv.grantRole(allow_contract_h, earnville.address, {"from": account})
    tx_r.wait(1)

    ##buy and sell

    return earnville, coin_token, rfv, holders_reward, treasury, dev


def setPoolPercentages():
    pass


def main():
    deploy_earnville_and_cointoken()
