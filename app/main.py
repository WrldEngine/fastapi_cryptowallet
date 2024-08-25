import uvicorn
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.core.database import init_models
from app.api import v1

tags_metadata = [
    {
        "name": "home",
        "description": "Home Endpoints",
    },
    {
        "name": "authentication",
        "description": "Operations with authentication. The **login** logic is also here",
    },
    {
        "name": "profile",
        "description": "Actions with user profile in **MVP**",
    },
    {
        "name": "wallets",
        "description": "Actions with user wallets inside **MVP** logic",
    },
    {
        "name": "transactor",
        "description": "External transaction actions with wallets",
    },
    {
        "name": "checker",
        "description": "External actions to get any information about wallets",
    },
]


def get_application() -> FastAPI:
    application = FastAPI(
        openapi_tags=tags_metadata,
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
    )

    application.include_router(v1)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = get_application()

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("app.main:app", host="127.0.0.1", reload=True)
