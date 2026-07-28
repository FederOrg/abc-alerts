"""
Persistencia de ofertas notificadas.

Guarda los idoferta ya enviados para evitar
recibir múltiples mails con la misma oferta.
"""


import json
import logging

from pathlib import Path


logger = logging.getLogger(__name__)



class Storage:
    """
    Maneja almacenamiento local de ofertas vistas.
    """


    def __init__(
        self,
        filename: str = "seen_offers.json"
    ):

        self.file = Path(
            filename
        )

        self._ensure_file()



    def _ensure_file(self):
        """
        Crea el archivo si no existe.
        """

        if not self.file.exists():

            self.file.write_text(
                "[]",
                encoding="utf-8"
            )



    def load(
        self
    ) -> set[int]:
        """
        Lee IDs ya enviados.
        """

        try:

            content = self.file.read_text(
                encoding="utf-8"
            )

            ids = json.loads(
                content
            )


            return set(
                ids
            )


        except Exception:

            logger.exception(
                "Error leyendo almacenamiento"
            )

            return set()



    def save(
        self,
        offers: list
    ):
        """
        Guarda nuevas ofertas notificadas.
        """

        current_ids = self.load()


        for offer in offers:

            current_ids.add(
                offer.idoferta
            )


        self.file.write_text(

            json.dumps(
                list(current_ids),
                indent=4
            ),

            encoding="utf-8"
        )



    def get_new_offers(
        self,
        offers: list
    ) -> list:
        """
        Filtra solamente ofertas
        nunca notificadas.
        """

        seen_ids = self.load()


        new_offers = []


        for offer in offers:

            if offer.idoferta not in seen_ids:

                new_offers.append(
                    offer
                )


        return new_offers