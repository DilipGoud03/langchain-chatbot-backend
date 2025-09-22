from fastapi import APIRouter, status, HTTPException, Depends
from models.user_addresses import UserAddress
from services.user_address import UserAddressService
from fastapi.responses import JSONResponse
from typing import Optional, Any, Literal
from services.jwt_service import JWTBearer
from fastapi.requests import Request

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.post('/{user_id:int}/address', summary="Create new user address")
def create_user_address(
    user_id: int,
    address: UserAddress,
    d: Any = Depends(JWTBearer())

) -> JSONResponse:
    try:
        response = UserAddressService().CreateNewAddress(user_id, address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(
        status_code=200, content=f"message: {response}"
    )


@router.get('/{user_id:int}/address/list', summary="Get user address list")
def get_user_address_list(
    user_id: int,
    d: Any = Depends(JWTBearer())
):
    try:
        response = UserAddressService().ReadUserAdrresses(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return response


@router.delete('/address/{id:int}')
def delete_user_address(id: int):
    try:
        response = UserAddressService().DeleteUserAddress(id)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=str(e)
        )
    return JSONResponse(
        content=response, status_code=200
    )
