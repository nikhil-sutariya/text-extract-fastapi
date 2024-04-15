from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class ExtractedDataBase(BaseModel):
    id: Optional[int] = None
    email: str
    file_name: str
    text_data: str

class DocumentUploadBase(BaseModel):
    email: str
    file: UploadFile
