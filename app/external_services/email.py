import os
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.settings import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USER,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_USER,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_FROM_NAME="GYBER",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__name__).parent.parent.parent / "templates",
    VALIDATE_CERTS=False,
)


async def send_email_async(subject: str, email_to: str, body: dict) -> FastMail:
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email.html")


async def send_reset_password_async(
    subject: str, email_to: str, body: dict
) -> FastMail:
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="reset.html")
