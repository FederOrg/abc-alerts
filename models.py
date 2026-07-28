"""
Modelos de datos utilizados por ABC Alerts.

Contiene estructuras internas de la aplicación
para evitar trabajar directamente con JSON.
"""


from dataclasses import dataclass
from typing import Optional



@dataclass
class ABCOffer:
    """
    Representa una oferta devuelta por la API ABC.
    """

    idoferta: int

    estado: str

    cargo: str

    areaincumbencia: str

    descnivelmodalidad: str

    descdistrito: str

    domiciliodesempeno: str

    observaciones: str

    finoferta: str


    @classmethod
    def from_dict(
        cls,
        data: dict
    ):
        """
        Convierte una respuesta JSON
        de ABC en un objeto Python.
        """

        return cls(

            idoferta=data.get(
                "idoferta",
                0
            ),

            estado=data.get(
                "estado",
                ""
            ),

            cargo=data.get(
                "cargo",
                ""
            ),

            areaincumbencia=data.get(
                "areaincumbencia",
                ""
            ),

            descnivelmodalidad=data.get(
                "descnivelmodalidad",
                ""
            ),

            descdistrito=data.get(
                "descdistrito",
                ""
            ),

            domiciliodesempeno=data.get(
                "domiciliodesempeno",
                ""
            ),

            observaciones=data.get(
                "observaciones",
                ""
            ),

            finoferta=data.get(
                "finoferta",
                ""
            ),
        )



@dataclass
class FilteredOffer:
    """
    Oferta compatible con las incumbencias
    del docente.

    Es el modelo utilizado por mailer.py
    y storage.py.
    """

    idoferta: int

    codigo: str

    cargo: str

    modalidad: str

    distrito: str

    domicilio: str

    finoferta: str

    observaciones: str



    @classmethod
    def from_offer(
        cls,
        offer: ABCOffer
    ):
        """
        Genera una oferta simplificada
        para notificaciones.
        """

        return cls(

            idoferta=offer.idoferta,

            codigo=offer.areaincumbencia,

            cargo=offer.cargo,

            modalidad=offer.descnivelmodalidad,

            distrito=offer.descdistrito,

            domicilio=offer.domiciliodesempeno.strip(),

            finoferta=offer.finoferta,

            observaciones=offer.observaciones,
        )