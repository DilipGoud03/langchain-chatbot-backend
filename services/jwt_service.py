import time
import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from decouple import config

# ------------------------------------------------------------
# Module: auth_middleware
# Description:
#   Provides JSON Web Token (JWT) based authentication middleware
#   for FastAPI endpoints. Validates Bearer tokens in incoming
#   requests and ensures session authenticity and expiration.
# ------------------------------------------------------------

load_dotenv()


# ------------------------------------------------------------
# Class: JWTBearer
# Description:
#   Custom FastAPI HTTPBearer middleware that:
#     - Extracts JWT from the Authorization header.
#     - Validates token format and expiration.
#     - Decodes token payload using configured SECRET_KEY & ALGORITHM.
# ------------------------------------------------------------
class JWTBearer(HTTPBearer):
    # ------------------------------------------------------------
    # Method: __call__
    # Description:
    #   Intercepts incoming requests and validates the Bearer token.
    #   - Ensures the token exists and follows the correct scheme.
    #   - Decodes and verifies the JWT for validity and expiry.
    # ------------------------------------------------------------
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)  # type: ignore

        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid or missing authentication")

        self.decode_jwt(credentials.credentials)
        return credentials

    # ------------------------------------------------------------
    # Method: decode_jwt
    # Description:
    #   Decodes and validates a JWT token.
    #   - Checks signature validity.
    #   - Ensures token has not expired.
    #   Raises:
    #     HTTPException: if token is invalid or expired.
    # ------------------------------------------------------------
    def decode_jwt(self, token: str):
        try:
            decoded = jwt.decode(
                token,
                str(config("SECRET_KEY")).strip(),
                algorithms=[str(config("ALGORITHM")).strip()]
            )

            # Check expiration manually in case token is still technically valid
            if decoded.get("exp", 0) < time.time():
                raise HTTPException(status_code=403, detail="Token expired")

            return decoded

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid token")
