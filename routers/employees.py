from fastapi import APIRouter, status, HTTPException, Depends
from models.employees import Employee, EmployeeLogin, EmployeeList, LoggedInEmployee, ReadEmployee
from services.employee import EmployeeService
from fastapi.responses import JSONResponse
from typing import Optional, Any, Literal
from services.jwt_service import JWTBearer

# ------------------------------------------------------------
# Router: Employee
# Description:
#   Handles all employee-related operations including:
#   - Signup and login
#   - Retrieving, updating, and deleting employee records
#   - Listing employees with pagination
# ------------------------------------------------------------
router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    responses={404: {"description": "Not found"}},
)


# ------------------------------------------------------------
# Endpoint: POST /signup
# Description:
#   Creates a new employee account.
# ------------------------------------------------------------
@router.post('/signup', summary="Create new employee")
def create_employee(employee_: Employee) -> JSONResponse:
    try:
        response = EmployeeService().create_employee(employee_)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return JSONResponse(
        status_code=200, content=f"message: {response}"
    )


# ------------------------------------------------------------
# Endpoint: POST /login
# Description:
#   Authenticates an employee and returns a JWT token.
# ------------------------------------------------------------
@router.post('/login')
def login(employee: EmployeeLogin) -> JSONResponse:
    try:
        token = EmployeeService().login(employee)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if token and token == "":
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    
    return JSONResponse(status_code=200, content={"token": token})


# ------------------------------------------------------------
# Endpoint: GET /
# Description:
#   Retrieves the currently authenticated employee’s information.
# ------------------------------------------------------------
@router.get('', response_model=LoggedInEmployee)
def get_current_employee(d: Any = Depends(JWTBearer())):
    employee = EmployeeService().get_current_employee()
    return employee


# ------------------------------------------------------------
# Endpoint: GET /{id}
# Description:
#   Retrieves details of a specific employee by ID.
# ------------------------------------------------------------
@router.get('/{id:int}', response_model=ReadEmployee)
def get_employee(id: int, d: Any = Depends(JWTBearer())):
    try:
        response = EmployeeService().read_employee(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


# ------------------------------------------------------------
# Endpoint: PUT /{id}
# Description:
#   Updates an employee record by ID.
# ------------------------------------------------------------
@router.put('/{id:int}', response_model=ReadEmployee)
def update_employee(
    id: int,
    data: Employee,
    d: Any = Depends(JWTBearer())
):
    try:
        response = EmployeeService().update_employee(id, data)  # type:ignore
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


# ------------------------------------------------------------
# Endpoint: GET /list
# Description:
#   Retrieves a paginated list of employees.
#   Supports filtering, sorting, and pagination options.
# ------------------------------------------------------------
@router.get('/list', response_model=EmployeeList)
def get_employees(
    filter: str = '',
    order_by: str = 'id',
    order_direction: Literal['desc', 'asc'] = 'desc',
    limit: int = 10,
    page: int = 1,
    d: Any = Depends(JWTBearer())
):
    try:
        response = EmployeeService().read_employees(
            filter,
            order_by,
            order_direction,
            limit,
            page
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return response


# ------------------------------------------------------------
# Endpoint: DELETE /{id}
# Description:
#   Deletes a specific employee record by ID.
# ------------------------------------------------------------
@router.delete('/{id:int}')
def delete_employee(id: int):
    try:
        response = EmployeeService().delete_employee(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return JSONResponse(content=response, status_code=200)
