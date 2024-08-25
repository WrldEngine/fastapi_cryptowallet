from fastapi import APIRouter
from .users import auth_router, profile_router
from .wallets import wallets_router, transactor_router, checker_router
from .home import home_router


v1 = APIRouter()

v1.include_router(home_router, prefix="", tags=["home"])
v1.include_router(auth_router, prefix="/users/auth", tags=["authentication"])
v1.include_router(profile_router, prefix="/users/profile", tags=["profile"])
v1.include_router(wallets_router, prefix="/wallets", tags=["wallets"])
v1.include_router(transactor_router, prefix="/transactor", tags=["transactor"])
v1.include_router(checker_router, prefix="/checker", tags=["checker"])
