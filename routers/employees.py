from fastapi import APIRouter, status, HTTPException, Depends
from models.employees import Employee, EmployeeLogin, EmployeeList, LoggedInEmployee, ReadEmployee
from services.employee import EmployeeService
from fastapi.responses import JSONResponse
from typing import Optional, Any, Literal
from services.jwt_service import JWTBearer

router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    responses={404: {"description": "Not found"}},
)


@router.post('/signup', summary="Create new employee")
def create_employee(employee_: Employee) -> JSONResponse:
    try:
        response = EmployeeService().CreateEmployee(employee_)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(
        status_code=200, content=f"message: {response}"
    )


@router.post('/login')
def login(employee: EmployeeLogin) -> JSONResponse:
    try:
        token = EmployeeService().Login(employee)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=str(e)
        )
    if token and token == "":
        raise HTTPException(
            status_code=400, detail="Invalid email or password."
        )
    return JSONResponse(
        status_code=200, content={"token": token}
    )


@router.get('', response_model=LoggedInEmployee)
def get_current_employee(d: Any = Depends(JWTBearer())):
    employee = EmployeeService().GetCurrentEmployee()
    return employee


@router.get('/{id:int}', response_model=ReadEmployee)
def get_employee(id: int, d: Any = Depends(JWTBearer())):
    try:
        response = EmployeeService().ReadEmployee(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.put('/{id:int}', response_model=ReadEmployee)
def update_employee(
    id: int,
    data: Employee,
    d: Any = Depends(JWTBearer())
):
    try:
        response = EmployeeService().UpdateEmployee(id, data)  # type:ignore
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


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
        response = EmployeeService().ReadEmployees(
            filter,
            order_by,
            order_direction,
            limit,
            page
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return response


@router.delete('/{id:int}')
def delete_employee(id: int):
    try:
        response = EmployeeService().DeleteEmployee(id)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=str(e)
        )
    return JSONResponse(
        content=response, status_code=200
    )
