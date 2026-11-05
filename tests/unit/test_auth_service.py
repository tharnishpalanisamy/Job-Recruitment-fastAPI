from types import SimpleNamespace
from unittest.mock import patch

import pytest

from app.exceptions import InvalidCredentialsException
from app.models import User
from app.schemas import UserCreate


@pytest.mark.asyncio
async def test_authenticate_user_success(
    auth_service,
    mock_user_repository,
    mock_refresh_token_service,
):
    user = SimpleNamespace(
        id=1,
        email="test@gmail.com",
        password_hash="hashed_password",
        role="JOB_SEEKER",
    )

    mock_user_repository.get_by_email.return_value = user

    mock_refresh_token_service.issue_refresh_token.return_value = "refresh-token"

    with (
        patch(
            "app.services.implementations.auth_service.verify_password",
            return_value=True,
        ),
        patch(
            "app.services.implementations.auth_service.create_access_token",
            return_value="access-token",
        ),
    ):
        result = await auth_service.authenticate_user(
            UserCreate(
                username="test",
                email="test@gmail.com",
                password="Password@123",
            )
        )

    assert result["access_token"] == "access-token"
    assert result["refresh_token"] == "refresh-token"
    assert result["user"] == user


@pytest.mark.asyncio
async def test_authenticate_user_not_found(
    auth_service,
    mock_user_repository,
):
    mock_user_repository.get_by_email.return_value = None

    payload = UserCreate(
        username="dummy",
        email="unknown@gmail.com",
        password="Password@123",
    )

    with pytest.raises(InvalidCredentialsException):
        await auth_service.authenticate_user(payload)


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(
    auth_service,
    mock_user_repository,
):
    user = SimpleNamespace(
        id=1,
        email="test@gmail.com",
        password_hash="hashed_password",
        role="JOB_SEEKER",
    )

    mock_user_repository.get_by_email.return_value = user

    with (
        patch(
            "app.services.implementations.auth_service.verify_password",
            return_value=False,
        ),
        pytest.raises(InvalidCredentialsException),
    ):
        await auth_service.authenticate_user(
            UserCreate(
                username="test",
                email="test@gmail.com",
                password="WrongPassword@123",
            )
        )


@pytest.mark.asyncio
async def test_create_user_success(
    auth_service,
    mock_user_repository,
    mock_db,
    mock_email_service,
):

    created_user = User(
        id=1,
        username="test",
        email="test@gmail.com",
        password_hash="hashed_password",
    )

    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.create.return_value = created_user

    with patch(
        "app.services.implementations.auth_service.hash_password",
        return_value="hashed_password",
    ):
        result = await auth_service.create_user(
            UserCreate(
                username="test",
                email="test@gmail.com",
                password="Password@123",
            )
        )

    assert result == created_user
