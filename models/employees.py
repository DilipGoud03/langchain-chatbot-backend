from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.employee_addresses import EmployeeAddress


class Employee(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    password: str
    employee_type: Optional[str] = ''


class ReadEmployee(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    employee_type: Optional[str] = ''
    addresses: List[EmployeeAddress] = []


class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str


class LoggedInEmployee(BaseModel):
    id: int
    email: str
    name: str
    employee_type: str

    class Config:
        from_attributes = True


class Meta(BaseModel):
    current_item: Optional[int]
    total_items: Optional[int]
    limit: Optional[int]
    page: Optional[int]


class EmployeeList(BaseModel):
    meta: Meta
    employees: List[ReadEmployee]
