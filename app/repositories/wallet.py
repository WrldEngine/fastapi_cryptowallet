from typing import Dict, List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from app.models import Wallet, User
from app.core.database import async_session
from app.external_services import WalletGeneratorService

from .base import AbsWalletRepository


class WalletRepository(AbsWalletRepository):
    """
    Repository class for Wallet model.
    """

    @classmethod
    async def create_from_user(cls, user: User) -> Wallet:
        """
        Create a new wallet for a user.
        """
        async with async_session() as session:
            try:
                wallet_generator = await WalletGeneratorService.generate()
                instance = Wallet(
                    user=user,
                    address=wallet_generator.secrets["evm"][0][0],
                    private_key=wallet_generator.secrets["evm"][0][1],
                    mnemonics=wallet_generator.mnemonics,
                )
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
                return instance
            except IntegrityError:
                await session.rollback()

    @classmethod
    async def recover_wallet_from_mnemonics(cls, mnemonics: str, user: User) -> Wallet:
        """
        Recover a wallet using mnemonics for a user.
        """
        async with async_session() as session:
            try:
                wallet_creds = await WalletGeneratorService.recover(mnemonics)
                instance = Wallet(
                    user=user,
                    address=wallet_creds["evm"][0][0],
                    private_key=wallet_creds["evm"][0][1],
                    mnemonics=mnemonics,
                    is_secure=False,
                )
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
                return instance
            except IntegrityError:
                await session.rollback()

    @classmethod
    async def update(cls, instances: Dict, **filters) -> Wallet:
        """
        Update an existing wallet.
        """
        async with async_session() as session:
            query = (
                update(Wallet)
                .values(**instances.model_dump())
                .filter_by(**filters)
                .returning(Wallet)
            )
            try:
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one()
            except IntegrityError:
                await session.rollback()

    @classmethod
    async def delete(cls, **filters) -> None:
        """
        Delete a wallet.
        """
        async with async_session() as session:
            try:
                await session.execute(delete(Wallet).filter_by(**filters))
                await session.commit()
            except IntegrityError:
                await session.rollback()

    @classmethod
    async def get_single_wallet(cls, **filters) -> Optional[Wallet]:
        """
        Get a single wallet by filters.
        """
        async with async_session() as session:
            row = await session.execute(select(Wallet).filter_by(**filters))
            return row.scalar_one_or_none()
