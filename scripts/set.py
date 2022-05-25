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
OWNER_ADDRESS = "0x9f5D865390eA7CB9a7BB581e67fa07F9C10722f1"
BUSD_ADDRESS = "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"  # "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"

## real busd "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
##----------------------objectives


def deploy_Contracts():
    ##set up
    account = get_account()
    busd_amount = Web3.toWei(1, "ether")
    spice_amount = Web3.toWei(1, "ether")
    # coin_token = CoinToken[-1]
    # BUSD_ADDRESS = coin_token.address

    ## deploy dev
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
    ## Deploy Spice
    spice = Spice[-1]
    print("deployed spice successfully")

    # comment out when deploying to mainner
    # tx_spice = dev.setSpice(spice.address, {"from": account, "gas_limit": 200000})
    # tx_spice.wait(1)

    ## set initial value
    # approve holder spend to busd
    busd_contract = interface.IERC20(BUSD_ADDRESS)
    tx_approve = busd_contract.approve(spice.address, busd_amount, {"from": account})
    tx_approve.wait(1)

    # call setInitial value function
    tx_setValue = spice.setInitalPoolValue(
        spice_amount, {"from": account, "gas_limit": 3000000}
    )
    tx_setValue.wait(1)

    # set apy
    # tx_apy = spice.setAPY(99, {"from": account, "gas_limit": 2000000})
    # tx_apy.wait(1)
    # print("Apy has been set")


def main():
    deploy_Contracts()
