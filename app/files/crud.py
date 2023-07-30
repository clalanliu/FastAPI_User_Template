from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
import app.files.models as models
import app.files.schemas as schemas


async def get_user_file_by_name(db: AsyncSession, *, filename: str, user_id: str):
    stmt = select(models.File).where(models.File.user_id == user_id).where(models.File.filename == filename)
    result = await db.execute(stmt)
    file = result.scalars().first()
    return file

async def get_file_by_id(db: AsyncSession, *, file_id: int):
    stmt = select(models.File).where(models.File.id == file_id)
    result = await db.execute(stmt)
    file = result.scalars().first()
    return file

async def get_files_for_user(db: AsyncSession, *, user_id: str):
    stmt = select(models.File).where(models.File.user_id == user_id)
    result = await db.execute(stmt)
    files = result.scalars().all()
    return files

async def delete_file(db: AsyncSession, *, file_id: int):
    stmt = delete(models.File).where(models.File.id == file_id)
    await db.execute(stmt)
    await db.commit()

async def create_file(db: AsyncSession, *, file: schemas.FileCreate):
    db_file = models.File(**file.dict())
    db.add(db_file)

    await db.commit()
    await db.refresh(db_file)

    return schemas.File(
        id=db_file.id,
        filename=db_file.filename,
        file_path=db_file.file_path
    )

