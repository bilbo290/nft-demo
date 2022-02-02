from brownie import network, AdvanceCollectible
import pytest
import time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
)
from scripts.advance_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # Act
    advanced_collectible, create_tx = deploy_and_create()
    time.wait(180)
    # Assert
    assert advanced_collectible.tokenCounter() == 1
