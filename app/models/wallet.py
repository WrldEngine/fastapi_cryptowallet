from typing import List
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Table, Column, ForeignKey, func


class Wallet(Base):
    address: Mapped[str] = mapped_column(String(128), unique=True)
    private_key: Mapped[str] = mapped_column(String(128), unique=True)
    mnemonics: Mapped[str] = mapped_column(String(128), unique=True)
    is_secure: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="wallets")
