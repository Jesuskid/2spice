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
BUSD_ADDRESS = "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"  # "0x035a87F017d90e4adD84CE589545D4a8C5B7Ec80"

##real busd "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
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

    ##set access and  ownership transfers-------------------------

    ##grand roles for wallets
    # grant spice allowed contracts role for holder's reward
    allow_contract_h = holders_reward.ALLOWED_CONTRACTS()
    default_admin = holders_reward.DEFAULT_ADMIN_ROLE()

    tx_h = holders_reward.grantRole(
        allow_contract_h, spice.address, {"from": account, "gas_limit": 3000000}
    )
    tx_h.wait(1)
    # transfer admin role to owners
    tx_hr = holders_reward.grantRole(
        default_admin, OWNER_ADDRESS, {"from": account, "gas_limit": 3000000}
    )
    tx_hr.wait(1)

    # grant spice allowed contracts role for rfv
    tx_r = rfv.grantRole(
        allow_contract_h, spice.address, {"from": account, "gas_limit": 3000000}
    )
    tx_r.wait(1)
    # transfer admin role to owners
    tx_rr = rfv.grantRole(
        default_admin, OWNER_ADDRESS, {"from": account, "gas_limit": 3000000}
    )
    tx_rr.wait(1)
    # grant spice allowed contracts role for treasury
    tx_t = treasury.grantRole(
        allow_contract_h, spice.address, {"from": account, "gas_limit": 3000000}
    )
    tx_t.wait(1)
    tx_t2 = rfv.grantRole(
        allow_contract_h, OWNER_ADDRESS, {"from": account, "gas_limit": 3000000}
    )
    tx_t2.wait(1)
    # transfer admin role to owners
    tx_tt = treasury.grantRole(
        default_admin, OWNER_ADDRESS, {"from": account, "gas_limit": 3000000}
    )
    tx_tt.wait(1)

    # test = rfv.transferTo(OWNER_ADDRESS, busd_amount)
    # test.wait(1)


def main():
    deploy_Contracts()
