import asyncio

from pydantic import ValidationError
from sqlalchemy import select

from app.core import UserRole, hash_password
from app.core.config import setting
from app.database.connection import AsyncSessionLocal, engine
from app.models import User
from app.schemas import UserCreate


async def create_admin(user_data: UserCreate) -> str:
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
                role=UserRole.ADMIN,
            )
            session.add(user)
            action = "created"
        else:
            user.username = user_data.username
            user.password_hash = hash_password(user_data.password)
            user.role = UserRole.ADMIN
            action = "updated"

        await session.commit()
        return action


async def main() -> None:
    values = {
        "ADMIN_EMAIL": setting.ADMIN_EMAIL,
        "ADMIN_USERNAME": setting.ADMIN_USERNAME,
        "ADMIN_PASSWORD": setting.ADMIN_PASSWORD,
    }
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise ValueError(
            f"Set the following environment variables in .env: {', '.join(missing)}"
        )

    try:
        user_data = UserCreate(
            username=setting.ADMIN_USERNAME,
            email=setting.ADMIN_EMAIL,
            password=setting.ADMIN_PASSWORD,
        )
    except ValidationError as exc:
        errors = "; ".join(error["msg"] for error in exc.errors(include_input=False))
        raise ValueError(f"Invalid admin details: {errors}") from exc

    try:
        action = await create_admin(user_data)
        print(f"Admin account {action}: {user_data.email}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())