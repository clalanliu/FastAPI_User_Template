from fastapi import FastAPI
from app.files.routes import router as file_router

from app.core.database import create_db_and_tables
from app.users.schemas import UserCreate, UserRead
from app.users.crud import fastapi_users, auth_backend

app = FastAPI()

app.include_router(file_router, prefix="/files", tags=["files"])

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
