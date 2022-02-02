from scripts.helpful_scripts import (
    fund_with_link,
    get_account,
    OPENSEA_URL,
    get_contract,
)
from brownie import AdvanceCollectible, config, network


def deploy_and_create():
    account = get_account()
    advance_collectible = AdvanceCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    fund_with_link(advance_collectible.address)
    create_tx = advance_collectible.createCollectible({"from": account})
    create_tx.wait(1)
    print("NFT has beeen created")
    return advance_collectible, create_tx


def main():
    deploy_and_create()
