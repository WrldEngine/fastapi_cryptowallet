from .base import Base
from pydantic import Field


class Token(Base):
    access_token: str
    refresh_token: str = Field(default=None)
    token_type: str = Field(default="Bearer")


class VerifyEmail(Base):
    verification_token: str
    is_verified: bool = Field(default=False)


class UpdateVerifiedEmail(Base):
    is_verified: bool
