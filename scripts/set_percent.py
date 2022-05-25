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


def main():
    account = get_account()
    spice = Spice[-1]
    tx = spice.setAPY(99, {"from": account})
    tx.wait(1)
    print("Apy has been set")
