from sqlalchemy import Column, Integer, String
from datetime import datetime
from db import Base
from sqlalchemy.orm import relationship
from sql.models.employee_addresses import employeeAddresses


# ------------------------------------------------------------
# Model: Employee
# Description:
#   Represents an employee record within the system.
#
#   Stores basic personal and authentication information, along with
#   timestamps for creation and updates. Establishes a relationship
#   with the employeeAddresses model for managing multiple addresses
#   per employee.
# ------------------------------------------------------------
class Employee(Base):
    __tablename__ = "employees"

    # --------------------------------------------------------
    # Column Definitions
    # --------------------------------------------------------

    id = Column(Integer, primary_key=True, index=True)                          # Unique employee identifier
    name = Column(String(255), nullable=False)                                  # Employee's full name
    email = Column(String(255), unique=True, index=True, nullable=False)        # Employee's email address (must be unique)
    password = Column(String(255), nullable=True, default=False)                # Hashed password for authentication
    employee_type = Column(String(255), nullable=True, default='employee')      # Type of employee (e.g., admin, staff)
    created_at = Column(String(255), default=datetime.now(), nullable=False)    # Timestamp of record creation
    updated_at = Column(String(255), nullable=False, onupdate=datetime.now())   # Timestamp of last update
    addresses = relationship(
        employeeAddresses,
        cascade="all,delete",
        backref='employees'
    )  # Relationship to employeeAddresses (one-to-many)
