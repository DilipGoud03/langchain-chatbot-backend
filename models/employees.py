from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.employee_addresses import EmployeeAddress

# ------------------------------------------------------------
# Model: Employee
# Description:
#   Schema for creating or updating an employee record.
#   Includes basic employee details such as name, email, and role.
# ------------------------------------------------------------
class Employee(BaseModel):
    id: Optional[int] = None             # Employee ID (auto-generated)
    name: str                            # Full name of the employee
    email: EmailStr                      # Employee email (validated format)
    password: str                        # Password (plain or hashed)
    employee_type: Optional[str] = ''    # Role/type (e.g., admin, staff)


# ------------------------------------------------------------
# Model: ReadEmployee
# Description:
#   Schema for retrieving employee details.
#   Excludes sensitive information like passwords.
# ------------------------------------------------------------
class ReadEmployee(BaseModel):
    id: Optional[int] = None             # Employee ID
    name: str                            # Employee full name
    email: EmailStr                      # Employee email
    employee_type: Optional[str] = ''    # Role/type of employee
    addresses: List[EmployeeAddress] = []  # List of associated addresses


# ------------------------------------------------------------
# Model: EmployeeLogin
# Description:
#   Schema used for employee login requests.
# ------------------------------------------------------------
class EmployeeLogin(BaseModel):
    email: EmailStr                      # Email used for login
    password: str                        # Plain text password for authentication


# ------------------------------------------------------------
# Model: LoggedInEmployee
# Description:
#   Represents an authenticated employee (JWT/session context).
# ------------------------------------------------------------
class LoggedInEmployee(BaseModel):
    id: int                              # Employee ID
    email: str                           # Employee email
    name: str                            # Employee name
    employee_type: str                   # Employee role/type

    class Config:
        from_attributes = True           # Enables ORM-to-Pydantic conversion


# ------------------------------------------------------------
# Model: Meta
# Description:
#   Metadata for paginated API responses.
# ------------------------------------------------------------
class Meta(BaseModel):
    current_item: Optional[int]          # Index of current item in pagination
    total_items: Optional[int]           # Total number of items
    limit: Optional[int]                 # Max items per page
    page: Optional[int]                  # Current page number


# ------------------------------------------------------------
# Model: EmployeeList
# Description:
#   Schema for paginated employee list responses.
# ------------------------------------------------------------
class EmployeeList(BaseModel):
    meta: Meta                           # Pagination details
    employees: List[ReadEmployee]        # List of employees in current page
