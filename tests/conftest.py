import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from app.core.config import setting
from app.database import get_db
from app.database.base import Base
from app.main import app

TEST_DATABASE_URL = setting.TEST_DATABASE_URL

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not configured")


test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(setup_database):

    async with test_engine.connect() as connection:
        transaction = await connection.begin()

        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        try:
            yield session
        finally:
            await session.close()

            if transaction.is_active:
                await transaction.rollback()


@pytest_asyncio.fixture
async def client(db_session):

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
