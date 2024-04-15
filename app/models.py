from sqlalchemy import Column, String, Integer, TIMESTAMP, text
from app.database import Base

class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), index=True)
    file_name = Column(String(100))
    text_data = Column(String())
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
