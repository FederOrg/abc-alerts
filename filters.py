"""
Filtros de ofertas compatibles con las incumbencias del docente.

La lógica compara:

oferta["descnivelmodalidad"]
        +
oferta["areaincumbencia"]

contra:

config.incumbencias
"""


import logging
from models import ABCOffer, FilteredOffer
from typing import Dict, List


logger = logging.getLogger(__name__)


def normalize_text(value: str) -> str:
    """
    Normaliza textos provenientes de la API.

    Evita problemas con:
    - mayúsculas/minúsculas
    - espacios
    - caracteres raros
    """

    if not value:
        return ""

    return (
        value
        .strip()
        .upper()
    )



def filter_offers(
    offers: List[ABCOffer],
    incumbencias: Dict[str, List[str]]
) -> List[FilteredOffer]:
    """
    Filtra ofertas compatibles.

    Ejemplo:

    Oferta:
    {
        "descnivelmodalidad": "SECUNDARIA",
        "areaincumbencia": "CCD"
    }

    Config:
    {
        "SECUNDARIA": [
            "CCD",
            "ECS"
        ]
    }

    Resultado:
        oferta válida
    """

    filtered = []


    for offer in offers:

        estado = normalize_text(
            offer.estado
        )

        if estado != "PUBLICADA":
            continue


        modalidad = normalize_text(
            offer.descnivelmodalidad
        )


        codigo = normalize_text(
            offer.areaincumbencia
        )


        if not modalidad:
            logger.warning(
                "Oferta sin modalidad. ID=%s",
                offer.idoferta
            )

            continue


        if not codigo:
            logger.warning(
                "Oferta sin incumbencia. ID=%s",
                offer.idoferta
            )

            continue



        modalidades_validas = incumbencias.get(
            modalidad,
            []
        )


        modalidades_validas = [
            normalize_text(x)
            for x in modalidades_validas
        ]


        if codigo in modalidades_validas:

            logger.info(
                "Oferta compatible encontrada: %s - %s",
                modalidad,
                codigo
            )

            filtered.append(
                FilteredOffer(
                    idoferta=offer.idoferta,
                    codigo=offer.areaincumbencia,
                    cargo=offer.cargo,
                    modalidad=offer.descnivelmodalidad,
                    distrito=offer.descdistrito,
                    domicilio=offer.domiciliodesempeno.strip(),
                    finoferta=offer.finoferta,
                    observaciones=offer.observaciones,
                )
            )


    return filtered