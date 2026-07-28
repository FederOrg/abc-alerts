from mailer import MailSender
from config import load_config
from models import FilteredOffer


config = load_config()


offers = [

    FilteredOffer(

        idoferta=12345,

        codigo="CCD",

        cargo="CONSTRUCCION DE CIUDADANIA",

        modalidad="SECUNDARIA",

        distrito="MERLO",

        domicilio="Escuela ejemplo",

        finoferta="2026-07-31T07:30:00Z",

        observaciones="Prueba"

    )

]


mailer = MailSender(config)


mailer.send(
    offers
)


print(
    "Mail enviado"
)