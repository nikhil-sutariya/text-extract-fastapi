from sqlalchemy.orm import Session
from app.models import ExtractedData
from app.schemas import ExtractedDataBase

def get_all_extracted_data(db: Session):
    return db.query(ExtractedData).all()

def create_extracted_data_instance(db: Session, data: ExtractedDataBase):
    instance_data = ExtractedData(email=data['email'], file_name=data['file_name'], text_data=data['extracted_text'])
    db.add(instance_data)
    db.commit()
    db.refresh(instance_data)
    return instance_data
