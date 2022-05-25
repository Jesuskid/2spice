##imports
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

##Immutable Variables
OWNER_ADDRESS = "0x8478F8c1d693aB4C054d3BBC0aBff4178b8F1b0B"
BUSD_ADDRESS = "0x035a87F017d90e4adD84CE589545D4a8C5B7Ec80"

##real busd "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
##----------------------objectives


def deploy_Contracts():
    ##set up
    account = get_account()
    busd_amount = Web3.toWei(1, "ether")
    spice_amount = Web3.toWei(1, "ether")
    # coin_token = CoinToken.deploy({"from": account})
    # BUSD_ADDRESS = coin_token.address

    # ## deploy dev
    # dev = Dev.deploy(OWNER_ADDRESS, BUSD_ADDRESS, {"from": account})
    # print("deployed dev successfully")
    # ## deploy HoldersReward
    # holders_reward = HoldersReward.deploy(BUSD_ADDRESS, {"from": account})
    # print("deployed holders successfully")
    # ## deploy RFV
    # rfv = RFV.deploy(BUSD_ADDRESS, {"from": account})
    # print("deployed rfv successfully")
    # ##deploy treasury
    # treasury = Treasury.deploy(BUSD_ADDRESS, {"from": account})
    # deploy dev
    dev = Dev[-1]
    print("deployed dev successfully")
    ## deploy HoldersReward
    holders_reward = HoldersReward[-1]
    print("deployed holders successfully")
    ## deploy RFV
    rfv = RFV[-1]
    print("deployed rfv successfully")
    ##deploy treasury
    treasury = Treasury[-1]
    print("deployed treasury successfully")
    print("deployed treasury successfully")
    ## Deploy Spice
    spice = Spice.deploy(
        Web3.toWei(1, "ether"),
        holders_reward.address,
        rfv.address,
        treasury.address,
        dev.address,
        BUSD_ADDRESS,
        OWNER_ADDRESS,
        99,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print("deployed spice successfully")


def main():
    deploy_Contracts()
