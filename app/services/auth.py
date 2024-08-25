from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, Header, Security
from fastapi.security import api_key

from jose import jwt, ExpiredSignatureError, JWTError

from app.core.settings import settings
from app.utils.hashing import verify_password
from app.repositories import UserRepository
from app.models import User


api_key_header = api_key.APIKeyHeader(name="Authorization")


class AuthService:

    @staticmethod
    async def get_current_user(
        user_service: Annotated[UserRepository, Depends(UserRepository)],
        token: str = Security(api_key_header),
    ) -> Optional[User]:

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could Not Validate Credentials",
        )

        try:
            payload = jwt.decode(
                token,
                settings.JWT_USER_SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            username = payload.get("sub")
            mode = payload.get("mode")

            if username is None or mode != "access_token":
                raise credentials_exception

        except ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token Has Been Expired")

        except JWTError:
            raise credentials_exception

        user = await user_service.get_single(username=username)
        if not user:
            raise credentials_exception

        return user

    @staticmethod
    async def get_access_by_refresh_token(
        user_service: Annotated[UserRepository, Depends(UserRepository)],
        refresh_token: str = Security(api_key_header),
    ) -> Optional[User]:

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could Not Validate Credentials",
        )

        try:
            payload = jwt.decode(
                refresh_token,
                settings.JWT_USER_SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            username = payload.get("sub")
            mode = payload.get("mode")

            if username is None or mode != "refresh_token":
                raise credentials_exception

        except ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token Has Been Expired")

        except JWTError:
            raise credentials_exception

        user = await user_service.get_single(username=username)
        if not user:
            raise credentials_exception

        return user
