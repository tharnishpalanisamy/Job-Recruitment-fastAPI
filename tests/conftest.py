import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.core import UserRole, hash_password
from app.core.config import setting
from app.database import get_db
from app.database.base import Base
from app.main import app
from app.models import *

TEST_DATABASE_URL = setting.TEST_DATABASE_URL

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(setup_database):
    async with test_engine.connect() as conn:
        transaction = await conn.begin()
        async with TestingSessionLocal(
            bind=conn,
            join_transaction_mode="create_savepoint",
        ) as session:
            yield session
        await transaction.rollback()


@pytest_asyncio.fixture
async def client(db_session):

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest_asyncio.fixture
async def admin_user(db_session):

    user = User(
        username="admin",
        email="admin@test.com",
        password_hash=hash_password("Admin@123"),
        role=UserRole.ADMIN,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def admin_token(client, admin_user):

    response = await client.post(
        "/api/v1/auth/login", json={"email": admin_user.email, "password": "Admin@123"}
    )

    return response.json()["access_token"]


@pytest_asyncio.fixture
async def recuiter_user(db_session):

    user = User(
        username="recuiter",
        email="recuiter@test.com",
        password_hash=hash_password("recuiter@123"),
        role=UserRole.RECRUITER,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def recruiter_token(client, recuiter_user):

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": recuiter_user.email, "password": "recuiter@123"},
    )

    return response.json()["access_token"]


@pytest_asyncio.fixture
async def user(db_session):

    user = User(
        username="user",
        email="user@test.com",
        password_hash=hash_password("user@123"),
        role=UserRole.USER,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def user_token(client, user):

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "user@123"},
    )

    return response.json()["access_token"]


@pytest_asyncio.fixture
async def job_seeker(db_session):

    user = User(
        username="job_seeker",
        email="job_seeker@test.com",
        password_hash=hash_password("job_seeker@123"),
        role=UserRole.USER,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def job_seeker_token(client, job_seeker):

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": job_seeker.email, "password": "job_seeker@123"},
    )

    return response.json()["access_token"]


@pytest_asyncio.fixture
def job_payload():
    return {
        "title": "Software Engineer",
        "description": "Software Engineer position",
        "requirements": "Python, FastAPI",
        "qualification": "BSc Computer Science",
        "experience_min": 2,
        "experience_max": 5,
        "salary_min": 60000,
        "salary_max": 95000,
        "employment_type": "full_time",
        "location": "Remote",
        "vacancies": 3,
    }


@pytest_asyncio.fixture
def job_seeker_payload():
    return {
        "full_name": "Arun Kumar",
        "phone": "3383450518",
        "date_of_birth": "1996-05-14",
        "qualification": "B.E.",
        "specialization": "Computer Science and Engineering",
        "experience_years": 4,
        "current_company": "Avanse Technologies",
        "current_designation": "Software Engineer",
        "current_salary": 850000,
    }
