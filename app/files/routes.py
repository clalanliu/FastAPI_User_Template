import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import fastapi_users

import app.files.crud as crud
import app.files.schemas as file_schemas
import app.users.schemas as user_schemas
from app.core.database import get_db
from app.core.config import UP_LODED_FILE_ROOT
from app.core.crud import current_active_user as current_user
from app.core.models import User

router = APIRouter()

@router.post("/files/", response_model=file_schemas.File)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(current_user)):
    try:
        existing_file = await crud.get_user_file_by_name(db, filename=file.filename, username=current_user.Name)
        if existing_file:
            raise HTTPException(status_code=400, detail="File with the same name already exists.")

        user_folder_path = os.path.join(UP_LODED_FILE_ROOT, current_user.username)

        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)

        file_location = os.path.join(user_folder_path, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())

        file_schema = file_schemas.FileCreate(filename=file.filename, file_path=file_location)
        db_file = await crud.create_file(db=db, file=file_schema)

        return db_file
    except HTTPException as he:
        raise he
    except IntegrityError:
        raise HTTPException(status_code=400, detail="File with the same name already exists.")
    except Exception as e:
        print(e)
        return {"error": str(e)}