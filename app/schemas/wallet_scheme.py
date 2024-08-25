from .base import Base
from pydantic import Field, field_validator
from fastapi import HTTPException, status

MAX_PHRASES_LIMIT = 12


class WalletViewModel(Base):
    address: str
    is_secure: bool
    private_key: str = Field(default=None)
    mnemonics: str = Field(default=None)


class WalletSecuredViewModel(Base):
    address: str
    is_secure: bool


class WalletUpdateModel(Base):
    is_secure: bool


class WalletRecoveryModel(Base):
    mnemonics: str

    @field_validator("mnemonics")
    def validate_mnemonics(cls, value):
        if len(value.split()) < MAX_PHRASES_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Phrases Should Contain At Least {MAX_PHRASES_LIMIT} Words",
            )
        return value
