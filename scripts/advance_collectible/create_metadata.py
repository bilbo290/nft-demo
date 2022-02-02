from pyparsing import col
from brownie import AdvanceCollectible, network
from scripts.helpful_scripts import get_types
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

types_to_image_uri = {}
def main():
    advanced_collectible = AdvanceCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        types = get_types(advanced_collectible.tokenIdtoTypes(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{types}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exist! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = types
            collectible_metadata["description"] = f"A cool {types} mesh"

            image_uri = None
            image_path = "./img/" + types.lower().replace("_", "-") + ".png"
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else types_to_image_uri[types]
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image_uri"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-circle.png" -> "circle.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
