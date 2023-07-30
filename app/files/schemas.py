from pydantic import BaseModel


class FileBase(BaseModel):
    filename: str

    class Config:
        from_attributes = True


class FileCreate(FileBase):
    user_id: str
    file_path: str


class File(FileBase):
    id: int
