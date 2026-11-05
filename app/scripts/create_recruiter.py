import asyncio

from pydantic import ValidationError
from sqlalchemy import select

from app.core import UserRole, hash_password
from app.core.config import setting
from app.database.connection import AsyncSessionLocal, engine
from app.models import User
from app.schemas import UserCreate


async def create_recruiter(user_data: UserCreate) -> str:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == user_data.email)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                username=user_data.username,
                email=str(user_data.email),
                password_hash=hash_password(user_data.password),
                role=UserRole.RECRUITER,
            )
            session.add(user)
            action = "created"
        else:
            user.username = user_data.username
            user.password_hash = hash_password(user_data.password)
            user.role = UserRole.RECRUITER
            action = "updated"

        await session.commit()
        return action


async def main() -> None:
    values = {
        "RECRUITER_EMAIL": setting.RECRUITER_EMAIL,
        "RECRUITER_USERNAME": setting.RECRUITER_USERNAME,
        "RECRUITER_PASSWORD": setting.RECRUITER_PASSWORD,
    }
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise ValueError(
            f"Set the following environment variables in .env: {', '.join(missing)}"
        )

    try:
        user_data = UserCreate(
            username=setting.RECRUITER_USERNAME,
            email=setting.RECRUITER_EMAIL,
            password=setting.RECRUITER_PASSWORD,
        )
    except ValidationError as exc:
        errors = "; ".join(error["msg"] for error in exc.errors(include_input=False))
        raise ValueError(f"Invalid recruiter details: {errors}") from exc

    try:
        action = await create_recruiter(user_data)
        print(f"Recruiter account {action}: {user_data.email}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
