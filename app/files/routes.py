from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import app.files.crud as crud
import app.files.schemas as schemas
from app.core.database import get_db

router = APIRouter()

@router.post("/files/", response_model=schemas.File)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        existing_file = await crud.get_file_by_name(db, filename=file.filename)
        if existing_file:
            raise HTTPException(status_code=400, detail="File with the same name already exists.")

        file_location = f"uploaded_files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())

        file_schema = schemas.FileCreate(filename=file.filename, file_path=file_location)
        db_file = await crud.create_file(db=db, file=file_schema)

        return db_file
    except HTTPException as he:
        raise he
    except IntegrityError:
        raise HTTPException(status_code=400, detail="File with the same name already exists.")
    except Exception as e:
        print(e)
        return {"error": str(e)}
