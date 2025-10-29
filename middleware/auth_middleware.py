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

# ------------------------------------------------------------
# Load environment variables and initialize global variables
# ------------------------------------------------------------
load_dotenv()

# Global variable to store the current authenticated employee
# Note: Global variables in async apps (like FastAPI) are risky.
#       Consider switching to contextvars for thread-safe usage.
global current_employee_var


# ------------------------------------------------------------
# Middleware: AuthMiddleware
# Description:
#   - Intercepts each incoming request.
#   - Validates the Authorization header for a Bearer JWT token.
#   - Decodes the token and loads the corresponding employee data.
#   - Makes the authenticated employee accessible globally.
# ------------------------------------------------------------
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        global current_employee_var
        current_employee_var = None  # Reset context for every request

        authorization = request.headers.get("Authorization")

        if authorization:
            try:
                # Expect header format: "Bearer <token>"
                authorization = authorization.split(" ")
                token_type = authorization[0]
                token = authorization[1]

                # Validate token type
                if token_type.lower() != "bearer":
                    raise HTTPException(status_code=401, detail="Invalid Authorization type")

                # Decode JWT to extract employee payload
                payload = jwt.decode(
                    token,
                    str(config("SECRET_KEY")).strip(),
                    algorithms=[str(config("ALGORITHM")).strip()],
                )

                # Fetch employee details using the ID from token payload
                employee = employee_crud.get_employee_by_id(
                    db.get_db(), payload.get("id", 0)
                )

                # Convert DB object to dictionary and then to Pydantic model
                employee_dict = LoggedInEmployeeSchema().dump(employee)
                logged_employee = LoggedInEmployee(**employee_dict)  # type: ignore

                # Store the logged-in employee globally
                current_employee_var = logged_employee

            except Exception:
                # On failure (invalid token, DB error, etc.), skip authentication silently
                current_employee_var = None
                pass  # In production, log this exception for debugging

        # Continue with the request-response cycle
        response = await call_next(request)
        return response


# ------------------------------------------------------------
# Helper function: get_current_employee
# Description:
#   - Returns the current authenticated employee.
#   - Returns None if no user is logged in or token validation failed.
# ------------------------------------------------------------
def get_current_employee():
    return current_employee_var
