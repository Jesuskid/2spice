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
    coin_token = "0x035a87F017d90e4adD84CE589545D4a8C5B7Ec80"
    rfv = "0x369611d7D7549Efe88e015A3F47311d6096dD8b9"
    holders_reward = "0x7d74f80EB6D919B1FCD09f58c84d3303Cc566b0A"
    treasury = "0x2C665742d25712E2Ddfe112Ca8333d3c285A1eFB"
    dev = "0xe0e426e64B3E4B4121Ca2cD89616220e63aBdb8D"
    spice = Spice.deploy(
        Web3.toWei(1000000, "ether"),
        holders_reward,
        rfv,
        treasury,
        dev,
        coin_token,
        99,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    busd_amount = Web3.toWei(1000000, "ether")
    xusd_amount = Web3.toWei(1000000, "ether")
    CoinToken[-1].approve(spice.address, busd_amount, {"from": account})
    spice.approve(spice.address, xusd_amount, {"from": account})
    tx = spice.setInitalPoolValue(busd_amount, {"from": account})
    tx.wait(1)
    tx2 = CoinToken[-1].transferFrom(
        account, holders_reward.address, busd_amount, {"from": account}
    )
    tx2.wait(1)
    print("set pool value")

    return spice, coin_token, rfv, holders_reward, treasury, dev


def main():
    deploy_earnville_and_cointoken()
