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
    interface,
)
from scripts.helpful_scripts import get_account
from web3 import Web3


def main():
    account = get_account()
    spice = Spice[-1]
    busd_contract = interface.IERC20("0x035a87F017d90e4adD84CE589545D4a8C5B7Ec80")
    busd = busd_contract.balanceOf(spice.address)
    tx = spice.priceOfXusdInBusd()
    bal = spice.totalSupply()
    print(tx)
    print(bal)
    print(busd)
    print(busd / bal)
    print("Apy has been set")
