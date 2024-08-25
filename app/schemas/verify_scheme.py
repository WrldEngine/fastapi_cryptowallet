from .base import Base
from pydantic import Field


class VerifyEmail(Base):
    verification_token: str
    is_verified: bool = Field(default=False)


class UpdateVerifiedEmail(Base):
    is_verified: bool
