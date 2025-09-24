import jwt
import time
from dotenv import load_dotenv
from sql.cruds import employees as employee_crud
from models.employees import LoggedInEmployee
from sql.schemas.employees import LoggedInEmployeeSchema
import db
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from decouple import config

load_dotenv()
global current_employee_var


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        global current_employee_var
        current_employee_var = None
        authorization = request.headers.get("Authorization")
        if authorization:
            try:
                authorization = authorization.split(" ")
                token = authorization[1]
                token_type = authorization[0]
                if token_type.lower() != "bearer":
                    raise HTTPException(status_code=401, detail=("Invalid Authorization type"))
                payload = jwt.decode(
                    token,
                    str(config("SECRET_KEY")).strip(),
                    algorithms=[str(config("ALGORITHM")).strip()],
                )
                employee = employee_crud.get_employee_by_id(
                    db.get_db(), payload.get("id", 0))
                employee_dict = LoggedInEmployeeSchema().dump(employee)
                logged_employee = LoggedInEmployee(**employee_dict) #type:ignore

                current_employee_var = logged_employee
            except Exception:
                current_employee_var = None
                pass

        response = await call_next(request)
        return response


def get_current_employee():
    return current_employee_var

def employee_has_role(role: str) -> bool:
    employee = get_current_employee()
    return bool(employee and hasattr(employee, 'employee_type') and employee.employee_type == role)
