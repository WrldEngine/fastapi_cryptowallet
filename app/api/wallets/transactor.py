import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.services import AuthService, PermissionService
from app.external_services import TransactionService
from app.schemas.transactor_scheme import (
    TransactorParsedData,
    SendTransactionModel,
    SendTransactionNativeModel,
    TransactionStatusModel,
)
from app.repositories import WalletRepository
from app.models import User

router = APIRouter()


@router.put("/send_native_transaction", response_model=TransactionStatusModel)
@PermissionService.verification_required
async def send_native_transaction(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    wallet_service: Annotated[WalletRepository, Depends(WalletRepository)],
    form_data: SendTransactionNativeModel,
) -> TransactionStatusModel:
    """
    Send a native cryptocurrency transaction.
    """
    try:
        wallet = await wallet_service.get_single_wallet(
            address=form_data.from_address, user=current_user
        )
        status_data = await TransactionService.send_native(
            mainnet=form_data.mainnet,
            from_private_key=wallet.private_key,
            from_address=form_data.from_address,
            to_address=form_data.to_address,
            amount=form_data.amount,
        )
        return TransactionStatusModel(status=status_data)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable To Make Transaction",
        )


@router.put("/send_transaction_erc20", response_model=TransactionStatusModel)
@PermissionService.verification_required
async def send_transaction_erc20(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    wallet_service: Annotated[WalletRepository, Depends(WalletRepository)],
    form_data: SendTransactionModel,
) -> TransactionStatusModel:
    """
    Send an ERC20 token transaction.
    """
    try:
        wallet = await wallet_service.get_single_wallet(
            address=form_data.from_address, user=current_user
        )
        status_data = await TransactionService.send_erc20(
            mainnet=form_data.mainnet,
            contract_address=form_data.contract_address,
            from_private_key=wallet.private_key,
            from_address=form_data.from_address,
            to_address=form_data.to_address,
            amount=form_data.amount,
        )
        return TransactionStatusModel(status=status_data)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable To Make Transaction ERC20",
        )


@router.put("/send_transaction_bep20", response_model=TransactionStatusModel)
@PermissionService.verification_required
async def send_transaction_bep20(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    wallet_service: Annotated[WalletRepository, Depends(WalletRepository)],
    form_data: SendTransactionModel,
) -> TransactionStatusModel:
    """
    Send a BEP20 token transaction.
    """
    try:
        wallet = await wallet_service.get_single_wallet(
            address=form_data.from_address, user=current_user
        )
        status_data = await TransactionService.send_bep20(
            mainnet=form_data.mainnet,
            contract_address=form_data.contract_address,
            from_private_key=wallet.private_key,
            from_address=form_data.from_address,
            to_address=form_data.to_address,
            amount=form_data.amount,
        )
        return TransactionStatusModel(status=status_data)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable To Make Transaction BEP20",
        )
