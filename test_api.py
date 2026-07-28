from config import load_config
from api import ABCClient


config = load_config()

client = ABCClient(config)


offers = client.fetch_all_offers()


print(
    f"Ofertas encontradas: {len(offers)}"
)


for offer in offers[:5]:

    print(
        offer
    )