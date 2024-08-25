import logging

from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Body, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.repositories import UserRepository
from app.services import ActionService, AuthService
from app.utils.security import create_access_token, create_refresh_token
from app.schemas.user_scheme import UserViewModel, UserCreationModel, UserAuthModel
from app.schemas.auth_scheme import Token

router = APIRouter()


@router.post("/signup", status_code=201, response_model=UserViewModel)
async def create_user(
    user: UserCreationModel,
    user_service: Annotated[UserRepository, Depends(UserRepository)],
) -> UserViewModel:
    """
    Create a new user account.

    Args:
        user (UserCreationModel): The user creation model containing the user's details.
        user_service (UserRepository): The user repository dependency.

    Returns:
        UserViewModel: The created user's view model.
    """
    try:
        user = await user_service.create(user)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="This Username Or Email Already Exists",
        )
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[UserAuthModel, Body(...)],
    user_service: Annotated[UserRepository, Depends(UserRepository)],
) -> Token:
    """
    Authenticate a user and return access and refresh tokens.

    Args:
        form_data (UserAuthModel): The user authentication model containing the username and password.
        user_service (UserRepository): The user repository dependency.

    Returns:
        Token: The access and refresh tokens.
    """
    user = await ActionService.authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username Or Password",
        )
    data = {"sub": user.username}
    return Token(
        access_token=create_access_token(data),
        refresh_token=create_refresh_token(data),
    )


@router.post("/login/refresh", response_model=Token)
async def get_refresh_token(
    current_user: Annotated[User, Depends(AuthService.get_access_by_refresh_token)],
) -> Token:
    """
    Refresh the access token using the refresh token.

    Args:
        current_user (User): The current authenticated user, retrieved using the refresh token.

    Returns:
        Token: The new access token.
    """
    return Token(access_token=create_access_token({"sub": current_user.username}))
