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

def main():
    Earnville = Earnville()