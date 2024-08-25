import logging
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.services import AuthService, PermissionService
from app.schemas.transactor_scheme import (
    SendTransactionModel,
    SendTransactionNativeModel,
    TransactionStatusModel,
)
from app.schemas.wallet_scheme import (
    WalletViewModel,
    WalletUpdateModel,
    WalletSecuredViewModel,
    WalletRecoveryModel,
)
from app.repositories import WalletRepository
from app.models import User

router = APIRouter()


@router.post("/create", status_code=201)
@PermissionService.verification_required
async def create_wallet(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    wallet_service: Annotated[WalletRepository, Depends(WalletRepository)],
) -> Any:
    """
    Create a new wallet for the current user.
    """
    try:
        await wallet_service.create_from_user(current_user)
        return status.HTTP_201_CREATED
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable To Create Wallet",
        )


@router.post("/recover", response_model=WalletViewModel)
@PermissionService.verification_required
async def recover_wallet(
    recover_data: WalletRecoveryModel,
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    wallet_service: Annotated[WalletRepository, Depends(WalletRepository)],
) -> WalletViewModel:
    """
    Recover a wallet using mnemonics for the current user.
    """
    try:
        return await wallet_service.recover_wallet_from_mnemonics(
            mnemonics=recover_data.mnemonics, user=current_user
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable To Recover Wallet",
        )


@router.get("/{address}", response_model=WalletSecuredViewModel)
async def get_wallet_information(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    wallet_service: Annotated[WalletRepository, Depends(WalletRepository)],
    address: str,
) -> WalletSecuredViewModel:
    """
    Get information about a specific wallet.
    """
    wallet = await wallet_service.get_single_wallet(address=address, user=current_user)
    if wallet is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="This Wallet Not Exists In Your Account",
        )
    return wallet


@router.get("/{address}/credentials", response_model=WalletViewModel)
@PermissionService.verification_required
async def get_wallet_credentials(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    wallet_service: Annotated[WalletRepository, Depends(WalletRepository)],
    address: str,
) -> WalletViewModel:
    """
    Get the credentials of a specific wallet.
    """
    instance = WalletUpdateModel(is_secure=False)
    try:
        return await wallet_service.update(instance, address=address, user=current_user)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable Access To Wallet",
        )


@router.delete("/{address}", status_code=200)
@PermissionService.verification_required
async def delete_wallet(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    wallet_service: Annotated[WalletRepository, Depends(WalletRepository)],
    address: str,
) -> Any:
    """
    Delete a specific wallet from the current user's account.
    """
    try:
        await wallet_service.delete(address=address, user=current_user)
        return status.HTTP_200_OK
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable Access To Wallet",
        )
