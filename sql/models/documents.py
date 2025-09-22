from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_path = Column(String(255), nullable=False)
    doc_path = Column(String(255), nullable=False)
    type = Column(String(50), unique=True, index=True, nullable=False)
    user = relationship("User")
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
