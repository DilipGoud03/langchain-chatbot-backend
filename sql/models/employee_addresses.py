from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


# ------------------------------------------------------------
# Model: employeeAddresses
# Description:
#   Stores address information associated with a specific employee.
#
#   Supports multiple addresses per employee and allows marking one
#   as the default address. Includes automatic creation and update
#   timestamps for record tracking.
# ------------------------------------------------------------
class employeeAddresses(Base):
    __tablename__ = 'employee_addresses'

    # --------------------------------------------------------
    # Column Definitions
    # --------------------------------------------------------

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)  # Linked employee ID
    address = Column(String(250), nullable=True)  # Street address or detailed location
    city = Column(String(50), nullable=True)      # City name
    state = Column(String(50), nullable=True)     # State or region
    zip_code = Column(String(50), nullable=True)  # Postal or ZIP code
    is_default = Column(Boolean, default=False)   # True if this is the default address

    created_at = Column(DateTime, default=datetime.now, nullable=False)  # Record creation timestamp
    updated_at = Column(DateTime, onupdate=datetime.now)                 # Record last update timestamp
    employee = relationship("Employee", backref="addresses")  # Relationship to the Employee model
