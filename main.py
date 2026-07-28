"""
Punto de entrada de la aplicación.

Flujo:

1. Cargar configuración
2. Consultar API ABC
3. Filtrar ofertas compatibles
4. Eliminar ofertas ya notificadas
5. Enviar mail
6. Guardar ofertas notificadas
"""

import logging
import sys

from api import ABCClient
from config import load_config
from filters import filter_offers
from mailer import MailSender
from storage import Storage


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main():

    logger.info("========================================")
    logger.info(" Iniciando búsqueda de ofertas ABC ")
    logger.info("========================================")

    try:

        # ----------------------------------------
        # Configuración
        # ----------------------------------------

        config = load_config()

        # ----------------------------------------
        # API
        # ----------------------------------------

        client = ABCClient(config)

        logger.info("Consultando API...")

        offers = client.fetch_all_offers()

        logger.info("Ofertas recibidas: %s", len(offers))

        # ----------------------------------------
        # Filtrar incumbencias
        # ----------------------------------------

        filtered = filter_offers(
            offers,
            config.incumbencias
        )

        logger.info(
            "Ofertas compatibles: %s",
            len(filtered)
        )

        if not filtered:
            logger.info("No existen ofertas compatibles.")
            return

        # ----------------------------------------
        # Ofertas ya notificadas
        # ----------------------------------------

        storage = Storage()

        print(type(filtered[0]))
        print(filtered[0])
        
        new_offers = storage.get_new_offers(filtered)

        logger.info(
            "Ofertas nuevas: %s",
            len(new_offers)
        )

        if not new_offers:
            logger.info(
                "No existen ofertas nuevas para notificar."
            )
            return

        # ----------------------------------------
        # Mail
        # ----------------------------------------

        logger.info("Enviando correo...")

        sender = MailSender(config)

        sender.send(new_offers)

        logger.info("Correo enviado correctamente.")

        # ----------------------------------------
        # Guardar IDs
        # ----------------------------------------

        storage.save(new_offers)

        logger.info("Ofertas almacenadas.")

        logger.info("Proceso finalizado correctamente.")

    except Exception:

        logger.exception(
            "Error inesperado durante la ejecución."
        )

        sys.exit(1)


if __name__ == "__main__":
    main()