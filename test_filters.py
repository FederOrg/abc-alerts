from config import load_config
from api import ABCClient
from filters import filter_offers


config = load_config()


client = ABCClient(config)


offers = client.fetch_all_offers()


filtered = filter_offers(
    offers,
    config.incumbencias
)


print(
    f"Compatibles: {len(filtered)}"
)


for offer in filtered:

    print(
        offer["idoferta"],
        offer["areaincumbencia"],
        offer["cargo"],
        offer["descdistrito"]
    )