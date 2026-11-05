import asyncio
from getpass import getpass

from pydantic import ValidationError
from sqlalchemy import select

from app.core import UserRole, hash_password
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
    try:
        email = input("Recruiter email: ").strip()
        username = input("Recruiter username: ").strip()
        password = getpass("Recruiter password: ")

        try:
            user_data = UserCreate(
                username=username,
                email=email,
                password=password,
            )
        except ValidationError as exc:
            print(f"Invalid recruiter details:\n{exc}")
            return

        action = await create_recruiter(user_data)
        print(f"Recruiter account {action}: {user_data.email}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
