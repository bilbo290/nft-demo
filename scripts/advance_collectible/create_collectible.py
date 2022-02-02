from brownie import AdvanceCollectible
from scripts.helpful_scripts import get_account, fund_with_link
from web3 import Web3


def main():
    account = get_account()
    advance_collectible = AdvanceCollectible[-1]
    fund_with_link(advance_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creation_transaction = advance_collectible.createCollectible({"from": account})
    creation_transaction.wait(1)
    print("Collectible created!")
