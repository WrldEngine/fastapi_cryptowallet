import re

from typing import List, Optional, Dict, Any
from pydantic import field_validator, EmailStr, Field, Extra, PrivateAttr
from fastapi import HTTPException, status

from lqd_services import AvailableChainNodes

from .base import Base
from .wallet_scheme import WalletSecuredViewModel

USERNAME_LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$")
MAX_PASSWORD_LENGTH = 5


class UserAuthModel(Base):
    username: str
    password: str


class UserCreationModel(Base):
    username: str
    password: str
    email: EmailStr

    @field_validator("username")
    def validate_username(cls, value):
        if not USERNAME_LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username Should Contain Only Letters",
            )
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < MAX_PASSWORD_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Password Can Not Contain Less Than {MAX_PASSWORD_LENGTH} Symbols",
            )
        return value


class UserViewModel(Base):
    id: int
    username: str
    email: EmailStr
    is_verified: bool


class AvailableChainNodesViewModel(Base):
    mainnet_list: List


class UserWalletsViewModel(Base):
    id: int
    username: str
    wallets: List[WalletSecuredViewModel]


class UserUpdateModel(Base):
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    is_verified: bool = Field(default=None)

    @field_validator("username")
    def validate_username(cls, value):
        if not USERNAME_LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username Should Contain Only Letters",
            )
        return value


class UserResetPassword(Base):
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < MAX_PASSWORD_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Password Can Not Contain Less Than {MAX_PASSWORD_LENGTH} Symbols",
            )
        return value


class UserChainsViewModel(Base):
    mainnet_dict: Dict | None


class UserSetChainModel(Base):
    mainnet: str
    gas: float

    @field_validator("mainnet")
    def validate_chains(cls, value):
        if value not in AvailableChainNodes:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unavailable Chain",
            )
        return value


class UserRemoveChainModel(Base):
    mainnet: str

    @field_validator("mainnet")
    def validate_chains(cls, value):
        if value not in AvailableChainNodes:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unavailable Chain",
            )
        return value
