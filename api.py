import ssl
import requests
from models import ABCOffer
from requests.adapters import HTTPAdapter
from datetime import datetime, timezone
from typing import List
import logging
import requests

logger = logging.getLogger(__name__)

class LegacyTLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()

        # Permitir cifrados antiguos del servidor ABC
        ctx.set_ciphers("ECDHE-RSA-AES256-SHA")

        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)

class ABCClient:
    """
    Cliente para consultar la API de ABC.
    """

    BASE_URL = (
        "https://servicios3.abc.gob.ar/valoracion.docente/api/"
        "apd.oferta.encabezado/select"
    )

    def __init__(self, config):
        self.config = config

    def fetch_all_offers(self) -> List[ABCOffer]:
        """
        Consulta todos los distritos configurados y devuelve
        una lista única de ofertas.
        """

        offers = []

        for distrito in self.config.distritos:

            logger.info(
                "Consultando distrito %s...",
                distrito
            )

            try:

                district_offers = self.fetch_district(distrito)

                logger.info(
                    "Distrito %s -> %s ofertas",
                    distrito,
                    len(district_offers)
                )

                offers.extend(
                    ABCOffer.from_dict(offer)
                    for offer in district_offers
                )

            except Exception as ex:

                logger.exception(
                    "Error consultando distrito %s: %s",
                    distrito,
                    ex
                )

        return offers

    def fetch_district(self, distrito: int) -> List[dict]:
        """
        Consulta un distrito.
        """

        now = (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )

        params = {
            "q": "*:*",
            "facet": "true",
            "facet.field": [
                "descdistrito",
                "descnivelmodalidad",
                "cargo",
                "estado",
            ],
            "facet.limit": 20,
            "facet.mincount": 1,
            "json.nl": "map",
            "wt": "json",
            "rows": 500,
            "start": 0,
            "sort": "finoferta asc",
            "fq": [
                "estado:Publicada",
                f"finoferta:[{now} TO *]",
                f"numdistrito:{distrito}",
            ],
        }

        session = requests.Session()
        session.mount("https://", LegacyTLSAdapter())

        response = session.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]["docs"]