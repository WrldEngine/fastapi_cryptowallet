import logging

from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from celery_tasks.tasks import send_email_verification_link, send_reset_password_token
from lqd_services import AvailableChainNodes

from app.models import User
from app.services import AuthService, ActionService
from app.utils.security import create_verification_token, create_reset_password_token
from app.repositories import UserRepository
from app.schemas.user_scheme import (
    UserViewModel,
    UserWalletsViewModel,
    UserUpdateModel,
    UserResetPassword,
    UserSetChainModel,
    UserRemoveChainModel,
    UserChainsViewModel,
    AvailableChainNodesViewModel,
)

router = APIRouter()


@router.get("/", response_model=UserViewModel)
async def get_profile(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    user_service: Annotated[UserRepository, Depends(UserRepository)],
) -> UserViewModel:
    """
    Retrieve the profile of the current authenticated user.
    """
    return current_user


@router.get("/wallets", response_model=UserWalletsViewModel)
async def get_wallets(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
) -> UserWalletsViewModel:
    """
    Retrieve the wallets of the current authenticated user.
    """
    return current_user


@router.get("/chains", response_model=UserChainsViewModel)
async def get_chains(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
) -> UserChainsViewModel:
    """
    Retrieve the blockchain chains associated with the current authenticated user.
    """
    return current_user


@router.put("/add_chain", response_model=UserChainsViewModel)
async def add_chain(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    user_service: Annotated[UserRepository, Depends(UserRepository)],
    form_data: UserSetChainModel,
) -> UserViewModel:
    """
    Add a blockchain chain to the current user's profile.
    """
    try:
        return await user_service.update_chains(
            form_data, type="add", id=current_user.id
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something Went Wrong",
        )


@router.delete("/remove_chain", response_model=UserViewModel)
async def remove_chain(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    user_service: Annotated[UserRepository, Depends(UserRepository)],
    form_data: UserRemoveChainModel,
) -> UserViewModel:
    """
    Remove a blockchain chain from the current user's profile.
    """
    try:
        return await user_service.update_chains(
            form_data, type="remove", id=current_user.id
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something Went Wrong",
        )


@router.get("/verify/{token}", status_code=200)
async def catch_verification_link(token: str) -> Any:
    """
    Verify the user's email using the provided token.
    """
    verify_user = await ActionService.verify_email(token=token)
    if not verify_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )
    return status.HTTP_200_OK


@router.put("/send_verification_message", status_code=200)
async def send_verification_message(
    request: Request,
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
) -> Any:
    """
    Send an email verification message to the current user.
    """
    try:
        verification_token = create_verification_token({"email": current_user.email})
        verification_link = (
            f"{request.base_url}users/profile/verify/{verification_token}"
        )
        send_email_verification_link.delay(
            link=verification_link, email=current_user.email
        )
        return status.HTTP_200_OK
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something Went Wrong",
        )


@router.patch("/reset_password", status_code=200)
async def reset_password(token: str, user_data: UserResetPassword) -> Any:
    """
    Reset the user's password using the provided token.
    """
    try:
        confirm_user_password = await ActionService.confirm_reset_password(
            token=token, user_instance=user_data
        )
        if not confirm_user_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token",
            )
        return status.HTTP_200_OK
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something Went Wrong",
        )


@router.put("/send_reset_password_token", status_code=200)
async def send_reset_password_token_message(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
) -> Any:
    """
    Send a reset password token to the user's email.
    """
    try:
        reset_password_token = create_reset_password_token(
            {"email": current_user.email}
        )
        send_reset_password_token.delay(
            token=reset_password_token, email=current_user.email
        )
        return status.HTTP_200_OK
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something Went Wrong",
        )


@router.patch("/edit", response_model=UserViewModel)
async def edit_user_data(
    form_data: UserUpdateModel,
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    user_service: Annotated[UserRepository, Depends(UserRepository)],
) -> UserViewModel:
    """
    Edit the current user's profile data.
    """
    try:
        if form_data.email is not None:
            form_data.is_verified = (
                current_user.email == form_data.email and current_user.is_verified
            )
        return await user_service.update(form_data, id=current_user.id)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something Went Wrong",
        )


@router.delete("/delete", status_code=200)
async def delete_user_data(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    user_service: Annotated[UserRepository, Depends(UserRepository)],
) -> Any:
    """
    Delete the current user's profile.
    """
    try:
        await user_service.delete(id=current_user.id)
        return status.HTTP_200_OK
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something Went Wrong",
        )
