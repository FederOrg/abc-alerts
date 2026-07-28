"""
Envío de notificaciones por correo.

Genera un mail HTML con las ofertas
compatibles encontradas.
"""


import logging
import smtplib

from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


logger = logging.getLogger(__name__)



class MailSender:
    """
    Responsable de enviar correos.
    """

    def __init__(self, config):

        self.config = config.mail



    def send(
        self,
        offers: list[dict]
    ):
        """
        Envía un correo con las ofertas encontradas.
        """

        html = self.build_html(
            offers
        )


        message = MIMEMultipart(
            "alternative"
        )

        message["From"] = (
            self.config.sender
        )

        message["To"] = ", ".join(
            self.config.recipients
        )


        message["Subject"] = (
            f"Alertas ABC - "
            f"{len(offers)} ofertas encontradas"
        )


        message.attach(
            MIMEText(
                html,
                "html",
                "utf-8"
            )
        )


        self.send_smtp(
            message
        )



    def send_smtp(
        self,
        message
    ):
        """
        Envía usando SMTP.
        """

        try:

            with smtplib.SMTP(
                self.config.smtp_server,
                self.config.smtp_port
            ) as server:

                server.starttls()

                
                print("CONFIG:", vars(self.config))
                print("SMTP SERVER:", self.config.smtp_server)
                print("SMTP PORT:", self.config.smtp_port)
                print("SMTP USER:", self.config.username)
                print("PASSWORD LENGTH:", len(self.config.password))
                
                

                server.login(
                    self.config.username,
                    self.config.password
                )


                server.sendmail(
                    self.config.sender,
                    self.config.recipients,
                    message.as_string()
                )


        except Exception:

            logger.exception(
                "Error enviando correo"
            )

            raise



    def build_html(
        self,
        offers: list[dict]
    ) -> str:
        """
        Construye la tabla HTML.
        """

        rows = ""


        for offer in offers:

            rows += f"""
            <tr>
                <td>{getattr(offer, "idoferta", "")}</td>
                <td>{getattr(offer, "codigo", "")}</td>
                <td>{getattr(offer, "cargo", "")}</td>
                <td>{getattr(offer, "modalidad", "")}</td>
                <td>{getattr(offer, "distrito", "")}</td>
                <td>{getattr(offer, "domicilio", "")}</td>
                <td>{getattr(offer, "finoferta", "")}</td>
                <td>{getattr(offer, "observaciones", "")}</td>
            </tr>
            """



        fecha = datetime.now().strftime(
            "%d/%m/%Y"
        )


        html = f"""
        <!DOCTYPE html>

        <html>

        <body>

        <h2>
            Alertas ABC - {fecha}
        </h2>


        <p>
            Se encontraron 
            <b>{len(offers)}</b>
            ofertas compatibles con tus incumbencias.
        </p>


        <table
            border="1"
            cellpadding="6"
            cellspacing="0"
            style="
                border-collapse: collapse;
                font-family: Arial;
                font-size: 12px;
            "
        >

        <thead>

        <tr>

            <th>ID Oferta</th>
            <th>Código</th>
            <th>Cargo</th>
            <th>Modalidad</th>
            <th>Distrito</th>
            <th>Domicilio</th>
            <th>Fin Oferta</th>
            <th>Observaciones</th>

        </tr>

        </thead>


        <tbody>

        {rows}

        </tbody>


        </table>


        <br>

        <small>
            Mensaje generado automáticamente por ABC Alerts.
        </small>


        </body>

        </html>
        """


        return html
