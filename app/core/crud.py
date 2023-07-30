from typing import AsyncGenerator, Optional
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.database import async_session_maker
from app.core.config import SECRET


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


#transport = BearerTransport(tokenUrl="auth/jwt/login")
transport = CookieTransport(cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=transport,
    get_strategy=get_jwt_strategy,
)
