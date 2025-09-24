from sqlalchemy import Column, Integer, String
from datetime import datetime
from db import Base
from sql.models.employee_addresses import employeeAddresses
from sqlalchemy.orm import relationship


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=True, default=False)
    employee_type = Column(String(255), nullable=True, default='employee')
    created_at = Column(String(255), default=datetime.now(), nullable=False)
    updated_at = Column(String(255), nullable=False, onupdate=datetime.now())
    addresses = relationship(employeeAddresses, cascade="all,delete", backref='employees')
