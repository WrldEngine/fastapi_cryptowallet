from datetime import timedelta, datetime
from jose import JWTError, jwt
from app.core.settings import settings


def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data["exp"] = expire
    data["mode"] = "access_token"

    encoded_jwt = jwt.encode(data, settings.JWT_USER_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    data["exp"] = expire
    data["mode"] = "refresh_token"

    encoded_jwt = jwt.encode(data, settings.JWT_USER_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def create_verification_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data["exp"] = expire
    encoded_jwt = jwt.encode(data, settings.JWT_VERIFY_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def create_reset_password_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data["exp"] = expire
    encoded_jwt = jwt.encode(
        data, settings.JWT_RESET_PASSWORD_SECRET_KEY, settings.ALGORITHM
    )

    return encoded_jwt
