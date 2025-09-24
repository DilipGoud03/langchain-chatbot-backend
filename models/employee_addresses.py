from pydantic import BaseModel
from typing import Optional, List

class EmployeeAddress(BaseModel):
    id: Optional[int] = None
    employee_id: int
    address: str
    city: str
    state: str
    zip_code: str
    is_default: bool = False