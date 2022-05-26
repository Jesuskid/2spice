import json
from brownie import accounts, config, network, CoinToken, Spice, interface
from scripts.helpful_scripts import get_account
from web3 import Web3

OWNER_ADDRESS = "0x8478F8c1d693aB4C054d3BBC0aBff4178b8F1b0B"
BUSD_ADDRESS = "0x035a87F017d90e4adD84CE589545D4a8C5B7Ec80"


def main():
    account = get_account()
    busd_amount = Web3.toWei(1, "ether")
    spice = Spice[-1]
    busd_contract = interface.IERC20(BUSD_ADDRESS)
    tx_approve = busd_contract.approve(spice.address, busd_amount, {"from": account})
    tx_approve.wait(1)

    tx = spice.buy(busd_amount, {"from": account, "gas_limit": 210000})
    tx.wait(1)
    print("rewarded")
