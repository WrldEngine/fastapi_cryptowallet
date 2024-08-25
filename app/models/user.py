from typing import List, Dict
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import PickleType
from sqlalchemy import String
from sqlalchemy.ext.mutable import MutableDict


class User(Base):
    username: Mapped[str] = mapped_column(String(1_000), unique=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    mainnet_dict: Mapped[Dict] = mapped_column(
        MutableDict.as_mutable(PickleType), nullable=True
    )
    wallets: Mapped[List["Wallet"]] = relationship(
        "Wallet", lazy="subquery", back_populates="user"
    )
