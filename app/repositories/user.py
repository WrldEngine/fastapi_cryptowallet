from typing import Dict, List, Optional

from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import array

from app.models import User
from app.core.database import async_session
from app.utils.hashing import hash_password

from .base import AbstractRepository


class UserRepository(AbstractRepository):
    """
    Repository class for User model.
    """

    @classmethod
    async def create(cls, instances: Dict) -> User:
        """
        Create a new user.
        """
        async with async_session() as session:
            try:
                instance = User(**instances.model_dump())
                instance.password = hash_password(instance.password)
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
                return instance
            except IntegrityError as e:
                await session.rollback()
                raise ValueError(f"Integrity error occurred: {e}")

    @classmethod
    async def update(cls, instances: Dict, **filters) -> User:
        """
        Update an existing user.
        """
        async with async_session() as session:
            query = (
                update(User)
                .values(**instances.model_dump(exclude_unset=True))
                .filter_by(**filters)
                .returning(User)
            )
            try:
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one()
            except IntegrityError as e:
                await session.rollback()
                raise ValueError(f"Integrity error occurred: {e}")

    @classmethod
    async def update_chains(cls, instance: Dict, type: str, **filters) -> User:
        """
        Update user's blockchain chains information.
        """
        async with async_session() as session:
            user_result_query = await session.execute(select(User).filter_by(**filters))
            user = user_result_query.scalar_one()

            if user.mainnet_dict is None:
                user.mainnet_dict = {}

            if type == "add":
                user.mainnet_dict.update({instance.mainnet: instance.gas})

            if type == "remove":
                del user.mainnet_dict[instance.mainnet]

            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            except IntegrityError as e:
                await session.rollback()
                raise ValueError(f"Integrity error occurred: {e}")

    @classmethod
    async def delete(cls, **filters) -> None:
        """
        Delete a user.
        """
        async with async_session() as session:
            try:
                await session.execute(delete(User).filter_by(**filters))
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise ValueError(f"Integrity error occurred: {e}")

    @classmethod
    async def get_single(cls, **filters) -> List[Optional[User]]:
        """
        Get a single user by filters.
        """
        async with async_session() as session:
            row = await session.execute(select(User).filter_by(**filters))
            return row.scalar_one_or_none()
