import logging
from typing import Annotated
from fastapi import APIRouter, Depends

from app.services import AuthService
from app.external_services import CheckerService
from app.schemas.checker_scheme import CheckerParsedData
from app.schemas.transactor_scheme import TransactorParsedData
from app.models import User

router = APIRouter()


@router.get("/{address}/{chain}", response_model=CheckerParsedData)
async def get_wallet_information_from_checker(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    address: str,
    chain: str,
) -> CheckerParsedData:
    """
    Retrieve wallet information from the checker service.

    Args:
        current_user (User): The current authenticated user, retrieved using AuthService.
        address (str): The wallet address to fetch information for.
        chain (str): The blockchain chain name.

    Returns:
        CheckerParsedData: Parsed data containing wallet balances and other details.
    """
    return await CheckerService.fetch_balances(address=address, chain_name=chain)


@router.get(
    "/{address}/{chain}/transactions", response_model=TransactorParsedData
)
async def get_wallet_transactions(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    address: str,
    chain: str,
) -> TransactorParsedData:
    """
    Retrieve wallet transactions from the checker service.

    Args:
        current_user (User): The current authenticated user, retrieved using AuthService.
        address (str): The wallet address to fetch transactions for.
        chain (str): The blockchain chain name.

    Returns:
        TransactorParsedData: Parsed data containing wallet transactions.
    """
    return await CheckerService.fetch_transactions(address=address, chain_name=chain)
