import json
from brownie import accounts, config, network, CoinToken, Spice
from scripts.helpful_scripts import get_account
from web3 import Web3


def main():
    account = get_account()
    spice = Spice[2]
    tx = spice.reward({"from": account})
    tx.wait(1)
    print("rewarded")
