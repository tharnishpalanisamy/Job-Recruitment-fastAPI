from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import setting

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int, role: str) -> str:
    now = datetime.now(UTC)

    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return jwt.encode(
        payload=payload, key=setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGORITHM
    )
