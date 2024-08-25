import logging

from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from lqd_services import AvailableChainNodes

from app.models import User
from app.services import AuthService
from app.schemas.user_scheme import AvailableChainNodesViewModel


router = APIRouter()


@router.get("/available_chains", response_model=AvailableChainNodesViewModel)
async def get_available_chains(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
) -> AvailableChainNodesViewModel:
    """
    Retrieve a list of available blockchain nodes for the authenticated user.

    This endpoint fetches and returns a list of available blockchain nodes
    that are supported by the application. The user must be authenticated
    to access this endpoint.

    Args:
        current_user (User): The current authenticated user, retrieved using
        the AuthService.

    Returns:
        AvailableChainNodesViewModel: A view model containing the list of
        available mainnet blockchain nodes.
    """
    return AvailableChainNodesViewModel(mainnet_list=AvailableChainNodes.keys())
