from typing import Optional

from jose import jwt
from fastapi import HTTPException, status

from app.core.settings import settings
from app.schemas.verify_scheme import UpdateVerifiedEmail
from app.schemas.user_scheme import UserResetPassword
from app.utils.hashing import verify_password, hash_password

from app.repositories import UserRepository
from app.models import User


class ActionService:

    @staticmethod
    async def confirm_reset_password(
        token: str,
        user_instance: UserResetPassword,
    ) -> bool:
        try:
            payload = jwt.decode(
                token, settings.JWT_RESET_PASSWORD_SECRET_KEY, settings.ALGORITHM
            )

            user_instance.password = hash_password(user_instance.password)
            await UserRepository.update(user_instance, email=payload.get("email"))

            return True

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token Has Been Expired")

        except Exception as e:
            return False

    @staticmethod
    async def verify_email(
        token: str,
    ) -> bool:

        try:
            payload = jwt.decode(
                token, settings.JWT_VERIFY_SECRET_KEY, settings.ALGORITHM
            )
            user_instance = UpdateVerifiedEmail(is_verified=True)
            await UserRepository.update(user_instance, email=payload.get("email"))

            return True

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Link Has Been Expired")

        except:
            return False

    @staticmethod
    async def authenticate_user(
        username: str,
        password: str,
    ) -> Optional[User]:
        user = await UserRepository.get_single(username=username)

        if not user:
            return False

        if not verify_password(password, user.password):
            return False

        return user
