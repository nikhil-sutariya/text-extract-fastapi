from typing import List
from fastapi import Depends, FastAPI, status, UploadFile, Form, File
from sqlalchemy.orm import Session
from app.repositories import get_all_extracted_data, create_extracted_data_instance
from app.models import Base
from app.schemas import ExtractedDataBase
from app.database import get_db, engine
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import asyncio
from app.services import extract_text_from_pdf, extract_text_from_doc, extract_text_from_docx, send_email

app = FastAPI()
Base.metadata.create_all(bind=engine)

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

async def text_extraction(data, db):
    file = data['file']
    file_extension = data['file_extension']
    data['file_name'] = file.filename
    
    if file_extension == "pdf":
        extracted_text = await extract_text_from_pdf(file.file)
    elif file_extension == "doc":
        extracted_text = await extract_text_from_doc(file.file)
    elif file_extension == "docx":
        extracted_text = await extract_text_from_docx(file.file)
    
    data['extracted_text'] = extracted_text
    response_data = create_extracted_data_instance(db=db, data=data)
    send_email("Extracion successful", data['email'], None)
    await asyncio.sleep(1)
    return response_data

@app.get("/get-uploaded-documents", response_model=List[ExtractedDataBase])
async def get_uploaded_documents(db: Session = Depends(get_db)):
    try:
        response_data = get_all_extracted_data(db)
        response = {
            "success": True, 
            "message": "Getting data of uploaded files.",
            "error_message": None,
            "data": response_data
        }
        response = jsonable_encoder(response)

    except Exception as e:
        response = {
            "success": False, 
            "message": "Something went wrong",
            "error_message": str(e),
            "data": None
        }

        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)

@app.post("/upload-document", response_model=List[ExtractedDataBase])
async def process_data(email: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        data = {'email': email, 'file': file}
        file_extension = file.filename.split(".")[1].lower()
        data['file_extension'] = file_extension
        if file_extension not in ALLOWED_EXTENSIONS:
            response = {
                "success": False,
                "message": "Unsupported file format. Please upload a PDF, DOC, or DOCX file",
                "error_message": None,
                "data": None
            }
            return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
        
        response_data = await text_extraction(data, db)

        response = {
            "success": True,
            "message": "Text data extracted successfully.",
            "error_message": None,
            "data": response_data
        }
        response = jsonable_encoder(response)

    except Exception as e:
        response = {
            "success": False,
            "message": "Something went wrong",
            "error_message": str(e),
            "data": None
        }
        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
