"""
Gestión de configuración de la aplicación.

Carga:
- config.yaml
- variables de entorno (.env)

Expone un objeto Config utilizado por
los distintos módulos.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import yaml
from dotenv import load_dotenv


# Cargar variables de entorno
load_dotenv()


@dataclass
class MailConfig:
    """
    Configuración SMTP.
    """

    smtp_server: str
    smtp_port: int
    username: str
    password: str
    sender: str
    recipients: List[str]


@dataclass
class ABCConfig:
    """
    Configuración completa de ABC Alerts.
    """

    distritos: List[int]

    modalidades: List[str]

    incumbencias: Dict[str, List[str]]

    mail: MailConfig



def load_config(
    path: str = "config.yaml"
) -> ABCConfig:
    """
    Carga configuración desde YAML.
    """

    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"No existe archivo {path}"
        )


    with open(
        config_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = yaml.safe_load(file)



    mail = MailConfig(

        smtp_server=os.getenv(
            "SMTP_SERVER",
            ""
        ),

        smtp_port=int(
            os.getenv(
                "SMTP_PORT",
                "587"
            )
        ),

        username=os.getenv(
            "SMTP_USERNAME",
            ""
        ),

        password=os.getenv(
            "SMTP_PASSWORD",
            ""
        ),

        sender=os.getenv(
            "MAIL_FROM",
            ""
        ),

        recipients=[
            x.strip()
            for x in os.getenv(
                "MAIL_TO",
                ""
            ).split(",")
            if x.strip()
        ],
    )


    return ABCConfig(

        distritos=data.get(
            "distritos",
            []
        ),

        modalidades=data.get(
            "modalidades",
            []
        ),

        incumbencias=data.get(
            "incumbencias",
            {}
        ),

        mail=mail
    )