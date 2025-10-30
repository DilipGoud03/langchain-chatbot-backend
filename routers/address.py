from fastapi import APIRouter, status, HTTPException, Depends
from models.employee_addresses import EmployeeAddress
from services.employee_address import EmployeeAddressService
from fastapi.responses import JSONResponse
from typing import Any
from services.jwt_service import JWTBearer
from fastapi.requests import Request


# ------------------------------------------------------------
# Router configuration for Employee-related address operations
# ------------------------------------------------------------
router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    responses={404: {"description": "Not found"}},
)


# ------------------------------------------------------------
# Endpoint: Create new employee address
# Description:
#   - Adds a new address for a specific employee.
#   - Requires authentication via JWTBearer.
# ------------------------------------------------------------
@router.post("/{employee_id:int}/address", summary="Create new employee address")
def create_employee_address(
    employee_id: int,
    address: EmployeeAddress,
    d: Any = Depends(JWTBearer())
) -> JSONResponse:
    try:
        response = EmployeeAddressService().create_employee_address(employee_id, address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": response},
    )


# ------------------------------------------------------------
# Endpoint: Get employee address list
# Description:
#   - Retrieves all saved addresses for a given employee.
#   - Only accessible for authenticated users.
# ------------------------------------------------------------
@router.get("/{employee_id:int}/address/list", summary="Get employee address list")
def get_employee_address_list(
    employee_id: int,
    d: Any = Depends(JWTBearer())
):
    try:
        response = EmployeeAddressService().read_employee_addresses(employee_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return response


# ------------------------------------------------------------
# Endpoint: Delete employee address by ID
# Description:
#   - Deletes a specific employee address using its ID.
#   - Can be restricted via authentication (recommended).
# ------------------------------------------------------------
@router.delete("/address/{id:int}", summary="Delete employee address by ID")
def delete_employee_address(
    id: int,
    d: Any = Depends(JWTBearer())
):
    try:
        response = EmployeeAddressService().delete_employee_address(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(
        content={"message": response},
        status_code=status.HTTP_200_OK,
    )
