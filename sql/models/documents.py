from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


# ------------------------------------------------------------
# Model: Document
# Description:
#   Represents an uploaded or processed document associated with
#   a specific employee record.
#
#   Stores both original and processed document paths, along with
#   document type and metadata for creation tracking.
# ------------------------------------------------------------
class Document(Base):
    __tablename__ = "documents"

    # --------------------------------------------------------
    # Column Definitions
    # --------------------------------------------------------

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    original_path = Column(String(255), nullable=False)  # Original uploaded document path
    doc_path = Column(String(255), nullable=False)        # Processed or stored document path
    type = Column(String(50), unique=True, index=True, nullable=False)  # e.g., 'public', 'private', etc.
    employee = relationship("Employee") # Relationship to the Employee model
    created_at = Column(DateTime, default=datetime.now, nullable=False) # Timestamp when the document was created
