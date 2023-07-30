from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import app.files.models as models
import app.files.schemas as schemas


async def get_user_file_by_name(db: AsyncSession, *, filename: str, user_id: str):
    stmt = select(models.File).where(models.File.username == user_id).where(models.File.filename == filename)
    result = await db.execute(stmt)
    file = result.scalars().first()
    return file


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
