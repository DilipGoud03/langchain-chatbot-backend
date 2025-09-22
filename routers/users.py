from fastapi import APIRouter, status, HTTPException, Depends
from models.users import User, UserLogin, UserList, LoggedInUser, ReadUser
from services.user import UserService
from fastapi.responses import JSONResponse
from typing import Optional, Any, Literal
from services.jwt_service import JWTBearer
from fastapi.requests import Request

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.post('/signup', summary="Create new user")
def create_user(user_: User) -> JSONResponse:
    try:
        response = UserService().CreateUser(user_)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(
        status_code=200, content=f"message: {response}"
    )


@router.post('/login')
def login(user: UserLogin) -> JSONResponse:
    try:
        token = UserService().LoginUser(user)
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


@router.get('', response_model=LoggedInUser)
def get_current_user(d: Any = Depends(JWTBearer())):
    user = UserService().GetCurrentUser()
    return user


@router.get('/{id:int}', response_model=ReadUser)
def get_user(id: int, d: Any = Depends(JWTBearer())):
    try:
        response = UserService().ReadUser(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.put('/{id:int}', response_model=ReadUser)
def update_user(
    id: int,
    data: User,
    d: Any = Depends(JWTBearer())
):
    try:
        response = UserService().UpdateUser(id, data)  # type:ignore
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return response


@router.get('/list', response_model=UserList)
def get_users(
    filter: str = '',
    order_by: str = 'id',
    order_direction: Literal['desc', 'asc'] = 'desc',
    limit: int = 10,
    page: int = 1,
    d: Any = Depends(JWTBearer())
):
    try:
        response = UserService().ReadUsers(
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
def delete_user(id: int):
    try:
        response = UserService().DeleteUser(id)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=str(e)
        )
    return JSONResponse(
        content=response, status_code=200
    )
