import os
from urllib.parse import urljoin
import urllib.request as urllib
import glob

import requests
from retry import retry
from dotenv import load_dotenv


def download_image(url, file_path, file_name):
    full_path = os.path.join(file_path, file_name)
    r = requests.get(url)
    with open(full_path, "wb") as f:
        f.write(r.content)
        
def copy_image(logo_path, file_path, file_name):
    full_path = os.path.join(file_path, file_name)
    os.system(f'copy {logo_path} {full_path}')

class BadRequestException(Exception):
    pass


class EndpointNotSupportedException(Exception):
    """
    Raised if status code in the 500 realm is raised by an API call in the cosmos metrics backend.
    Means the specific endpoint is not available for that chain.
    """

    pass


@retry(BadRequestException, delay=2.5, tries=3)
def request_lcd_json(endpoint: str, timeout=None) -> dict:
    r = requests.get(url=endpoint, timeout=timeout)
    if r.status_code == 200:
        return r.json()
    elif r.status_code in [501, 404, 524, 502]:
        raise EndpointNotSupportedException(
            f"{endpoint} is not supported or offline. - status code {r.status_code}"
        )
    else:
        raise BadRequestException(
            f"{endpoint} has not responeded - status code {r.status_code}"
        )


def get_networks_validator_registry(validator_name: str) -> list:
    VALIDATOR_URL = "https://validators.cosmos.directory"
    validator_url = urljoin(VALIDATOR_URL, validator_name)
    return request_lcd_json(validator_url, timeout=30)["validator"]["chains"]


if __name__ == "__main__":
    load_dotenv()

    directory = os.getenv("CHAINLIST_DIRECTORY_PATH")
    networks = get_networks_validator_registry(os.getenv("VALIDATOR_REGISTRY_NAME"))

    if os.getenv("LOGO_LOCAL"):
        logo_url = os.getenv("LOGO_LOCAL")
        local = True
    elif not os.getenv("LOGO_URL"):
        logo_url = networks[0]["image"]
        local = False
    else:
        logo_url = os.getenv("LOGO_URL")
        local = False

    for network in networks:
        network_name = network["name"]
        print(network_name)
        valoper_address = network["address"]
        file_name = f"{valoper_address}{logo_url[-4:]}"

        exception_lut = {
            "omniflixhub": "omniflix",
            "secretnetwork": "secret",
            "impacthub": "ixo",
            "gravitybridge": "gravity-bridge",
            "kichain": "ki-chain",
            "lumnetwork": "lum",
            "mars": "mars-protocol",
            "terra2": "terra",
            "cosmoshub": "cosmos",
        }
        if network_name in exception_lut:
            network_name = exception_lut[network_name]

        file_path = os.path.join(directory, "chain", network_name, "moniker")
        full_path = os.path.join(file_path, file_name)

        try:
            current_files = glob.glob(f"{full_path[:-4]}*")
            for file in current_files:
                os.remove(file)
            if not local:
                download_image(logo_url, file_path, file_name)
            else:
                copy_image(logo_url, file_path, file_name)
        except Exception as e:
            print(
                f"This is not a chain supported by the Chainlist -- {network_name} -- ",
                {e},
            )
