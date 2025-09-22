import jwt
import time
from dotenv import load_dotenv
from sql.cruds import users as user_crud
from models.users import LoggedInUser
from sql.schemas.users import LoggedInUserSchema
import db
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from decouple import config

load_dotenv()
global current_user_var


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        global current_user_var
        current_user_var = None
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
                user = user_crud.get_user_by_id(
                    db.get_db(), payload.get("id", 0))
                user_dict = LoggedInUserSchema().dump(user)
                logged_user = LoggedInUser(**user_dict)

                current_user_var = logged_user
            except Exception:
                current_user_var = None
                pass

        response = await call_next(request)
        return response


def get_current_user():
    print("Current User Var:", current_user_var)
    return current_user_var
