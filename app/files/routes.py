import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import app.files.crud as crud
import app.files.schemas as file_schemas
import app.users.schemas as user_schemas
from app.core.database import get_db
from app.core.config import UP_LODED_FILE_ROOT
from app.users.crud import current_active_user as current_user
from app.users.models import User

router = APIRouter()

@router.post("/files/", response_model=file_schemas.File)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(current_user)):
    try:
        user_folder_path = os.path.join(UP_LODED_FILE_ROOT, str(current_user.id))
        file_location = os.path.join(user_folder_path, file.filename)
        existing_file = await crud.get_user_file_by_name(db, filename=file.filename, user_id=str(current_user.id))
        if existing_file:
            os.remove(file_location)
            # if file data is stored in the db, we need to delete it before we can replace it
            await crud.delete_file(db=db, file_id=existing_file.id)

        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)

        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())

        file_schema = file_schemas.FileCreate(filename=file.filename, file_path=file_location, user_id=str(current_user.id))
        db_file = await crud.create_file(db=db, file=file_schema)

        return db_file
    except HTTPException as he:
        raise he
    except IntegrityError:
        raise HTTPException(status_code=400, detail="File with the same name already exists.")
    except Exception as e:
        print(e)
        return {"error": str(e)}
    
    
@router.get("/files/", response_model=List[file_schemas.File])
async def list_files(db: Session = Depends(get_db), current_user=Depends(current_user)):
    try:
        files = await crud.get_files_for_user(db, user_id=str(current_user.id))
        files = [file_schemas.File(**f.__dict__) for f in files]
        return files
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/files/{file_id}", response_model=file_schemas.File)
async def delete_file(file_id: int, db: Session = Depends(get_db), current_user=Depends(current_user)):
    try:
        file_to_delete = await crud.get_file_by_id(db, file_id=file_id)
        if not file_to_delete:
            raise HTTPException(status_code=404, detail="File not found")
        
        if file_to_delete.user_id != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not enough permissions")

        await crud.delete_file(db, file_id=file_id)

        # Optionally, you can also delete the actual file from disk
        os.remove(file_to_delete.file_path)

        return file_schemas.File(**file_to_delete.__dict__)
    
    except HTTPException as he:
        raise he
    except Exception as e:
        print(e)
        return {"error": str(e)}