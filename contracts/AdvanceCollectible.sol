// SDPX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvanceCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    uint256 public tokenId;
    enum Types {
        circle,
        wedg,
        diamond
    }
    mapping(uint256 => Types) public tokenIdtoTypes;
    mapping(bytes32 => address) public requestIdtoSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event typesAssigned(uint256 indexed tokenId, Types types);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Mesh", "Shape")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdtoSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Types types = Types(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdtoTypes[newTokenId] = types;
        emit typesAssigned(tokenId, types);
        address owner = requestIdtoSender[requestId];
        _safeMint(owner, newTokenId);
        //_setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // circle, wedg, diamond
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner or approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
