
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.files.models import Base as file_base
from app.core.config import DATABASE_URL
from app.core.models import Base



engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(file_base.metadata.create_all)


async def get_db() -> AsyncSession:
    db: AsyncSession = async_session_maker()
    try:
        yield db
    finally:
        await db.close()
