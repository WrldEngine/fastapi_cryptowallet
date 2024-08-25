from functools import wraps
from fastapi import HTTPException, status


class PermissionService:

    @staticmethod
    def verification_required(func):
        @wraps(func)
        async def has_permission(**kwargs):
            current_user = kwargs["current_user"]

            if not current_user.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You Are Not Verified User",
                )

            return await func(**kwargs)

        return has_permission

    @staticmethod
    def superuser_required(func):
        @wraps(func)
        async def has_permission(**kwargs):
            current_user = kwargs["current_user"]

            if not current_user.is_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You Are Not SuperUser",
                )

            return await func(**kwargs)

        return has_permission
