import time
import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from decouple import config


load_dotenv()


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)  # type: ignore

        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid or missing authentication")

        self.decode_jwt(credentials.credentials)
        return credentials

    def decode_jwt(self, token: str):
        try:
            decoded = jwt.decode(token, str(config("SECRET_KEY")).strip(), algorithms=[
                str(config("ALGORITHM")).strip()])
            if decoded.get("exp", 0) < time.time():
                raise HTTPException(status_code=403, detail="Token expired")
            return decoded
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid token")

