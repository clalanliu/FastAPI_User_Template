from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends

from app.users.models import UserManager
from app.core.crud import get_user_db

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)