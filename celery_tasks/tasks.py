import asyncio

from celery import Celery, shared_task

from app.core.settings import settings
from app.external_services.email import send_email_async, send_reset_password_async


redis_url = settings.build_redis_dsn()

celery = Celery(__name__, broker=redis_url, backend=redis_url)


@shared_task
def send_email_verification_link(link: str, email: str):
    body = {
        "title": "Verification Message",
        "link": link,
    }

    asyncio.get_event_loop().run_until_complete(send_email_async("Hello", email, body))


@shared_task
def send_reset_password_token(token: str, email: str):
    body = {
        "title": "Reset Password",
        "token": token,
    }

    asyncio.get_event_loop().run_until_complete(
        send_reset_password_async("Hello", email, body)
    )
