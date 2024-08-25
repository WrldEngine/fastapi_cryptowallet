import pytest

from .conftest import async_client
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuth:

    @pytest.mark.parametrize(
        "username, password, email, status",
        [
            ("testuser", "testpassword", "user@gmail.com", 201),
            ("anotheruser", "testpassword", "new_user@gmail.com", 201),
            ("test_cli", "test_password", "user@gmail.com", 422),
            ("testuser", "test_password", "usergmail.com", 422),
            ("testuser", "testpassword", "user@gmail.com", 503),
        ],
    )
    async def test_create_user(
        self, username, password, email, status, async_client: AsyncClient
    ):
        response = await async_client.post(
            "/users/auth/signup",
            json={
                "username": username,
                "password": password,
                "email": email,
            },
        )

        assert response.status_code == status

    @pytest.mark.parametrize(
        "username, password, status",
        [
            ("testuser", "testpassword", 200),
            ("testuser", "sdsssss", 401),
            ("testuseras", "testpassword", 401),
        ],
    )
    async def test_login(self, username, password, status, async_client: AsyncClient):
        response = await async_client.post(
            "/users/auth/login",
            json={"username": username, "password": password},
        )

        assert response.status_code == status

        if response.status_code == 200:
            return response.json()

    @pytest.mark.parametrize(
        "username, password, status",
        [
            ("testuser", "testpassword", 200),
            ("testuser", "sdsssss", 401),
        ],
    )
    async def test_login_refresh(
        self, username, password, status, async_client: AsyncClient
    ):
        try:
            data = await self.test_login(username, password, status, async_client)
            response = await async_client.post(
                f"/users/auth/login/refresh?refresh_token={data.get('access_token')}",
            )

            assert response.status_code == status

            if response.status_code == 200:
                return response.json()["refresh_token"] == "null"

        except:
            with pytest.raises(Exception) as exc_info:
                raise Exception(exc_info)


@pytest.mark.asyncio
class TestProfile:

    @pytest.mark.parametrize(
        "username, password, status",
        [
            ("testuser", "testpassword", 200),
            ("testuser", "sdsssss", 401),
        ],
    )
    async def test_get_profile(
        self, username, password, status, async_client: AsyncClient
    ):

        if status == 200:
            data = await TestAuth().test_login(username, password, status, async_client)

            headers = {
                "Authorization": data.get("access_token"),
            }

            response = await async_client.get(
                f"/users/profile/",
                headers=headers,
            )

            assert response.status_code == status

            if response.status_code == 200:
                assert response.json()["username"] == username

    @pytest.mark.parametrize(
        "username, password, status, email",
        [
            ("testuser", "testpassword", 200, "anotheremail@email.com"),
            ("anotheruser", "testpassworddd", 401, "anotheremail@email.com"),
            ("anotheruser", "testpassword", 500, "anotheremail@email.com"),
        ],
    )
    async def test_edit_profile(
        self, username, password, status, email, async_client: AsyncClient
    ):

        if status == 200:
            data = await TestAuth().test_login(username, password, status, async_client)

            headers = {
                "Authorization": data.get("access_token"),
            }

            response = await async_client.patch(
                f"/users/profile/edit",
                headers=headers,
                json={"email": email},
            )

            assert response.status_code == status

            if response.status_code == 200:
                assert response.json()["username"] == username
                assert response.json()["is_verified"] == False
                assert response.json()["email"] == email
