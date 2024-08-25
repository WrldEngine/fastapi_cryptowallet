import pytest
from httpx import AsyncClient

from .conftest import async_client


@pytest.mark.asyncio
class TestWallet:

    @pytest.mark.parametrize(
        "username, password, status, wallet_status",
        [
            ("testuser", "testpassword", 200, 403),
            ("testuser", "sdsssss", 401, 403),
        ],
    )
    async def test_create_wallet(
        self, username, password, status, wallet_status, async_client: AsyncClient
    ): ...
