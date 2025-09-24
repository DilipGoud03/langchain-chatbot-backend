from fastapi import APIRouter, status, HTTPException, Depends
from models.employee_addresses import EmployeeAddress
from services.employee_address import EmployeeAddressService
from fastapi.responses import JSONResponse
from typing import Optional, Any, Literal
from services.jwt_service import JWTBearer
from fastapi.requests import Request

router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    responses={404: {"description": "Not found"}},
)


@router.post('/{employee_id:int}/address', summary="Create new employee address")
def create_employee_address(
    employee_id: int,
    address: EmployeeAddress,
    d: Any = Depends(JWTBearer())

) -> JSONResponse:
    try:
        response = EmployeeAddressService().CreateNewAddress(employee_id, address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(
        status_code=200, content=f"message: {response}"
    )


@router.get('/{employee_id:int}/address/list', summary="Get employee address list")
def get_employee_address_list(
    employee_id: int,
    d: Any = Depends(JWTBearer())
):
    try:
        response = EmployeeAddressService().ReadEmployeeAdrresses(employee_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return response


@router.delete('/address/{id:int}')
def delete_employee_address(id: int):
    try:
        response = EmployeeAddressService().DeleteEmployeeAddress(id)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=str(e)
        )
    return JSONResponse(
        content=response, status_code=200
    )
