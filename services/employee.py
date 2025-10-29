import db
from sql.cruds import employees as employee_crud
import jwt
from datetime import datetime, timedelta
from decouple import config
from dotenv import load_dotenv
from middleware.auth_middleware import get_current_employee

load_dotenv()


class EmployeeService:
    """Service layer for handling employee-related operations."""

    def __init__(self):
        self.__db = db.get_db()

    # ------------------------------------------------------------
    # Method: CreateEmployee
    # Description:
    #   Creates a new employee record in the database.
    #   - Checks if an email already exists.
    #   - Inserts new employee data if unique.
    # ------------------------------------------------------------
    def CreateEmployee(self, employee_data):
        try:
            employee = employee_crud.get_employee_by_email(self.__db, employee_data.email)
            if employee:
                raise ValueError("Please use a different email address.")
            employee_crud.create_employee(self.__db, employee_data)
            return "Employee has been created successfully."
        except Exception as e:
            raise LookupError(str(e))

    # ------------------------------------------------------------
    # Method: Login
    # Description:
    #   Authenticates an employee by email and password.
    #   - Validates credentials.
    #   - Returns a JWT token valid for 1 day if successful.
    # ------------------------------------------------------------
    def Login(self, employee_data):
        try:
            employee_name = employee_data.email
            password = employee_data.password
            employee = employee_crud.get_employee_by_email(self.__db, employee_name)
            token = None

            if employee:
                if employee_crud._check_password(password, employee.password):
                    token = jwt.encode(
                        {
                            "exp": datetime.utcnow() + timedelta(days=1),
                            "iat": datetime.utcnow(),
                            "email": employee.email,
                            "id": employee.id,
                        },
                        str(config("SECRET_KEY")),
                        str(config("ALGORITHM"))
                    )
                else:
                    raise ValueError("Invalid employee username or password")

            if token is None:
                raise ValueError("Invalid employee username or password")

            return token
        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: GetCurrentEmployee
    # Description:
    #   Retrieves the currently authenticated employee.
    # ------------------------------------------------------------
    def GetCurrentEmployee(self):
        try:
            employee = get_current_employee()
            return employee
        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: ReadEmployee
    # Description:
    #   Fetches a specific employee's details by ID.
    # ------------------------------------------------------------
    def ReadEmployee(self, id: int):
        try:
            employee = employee_crud.get_employee_by_id(self.__db, id)
            if not employee:
                raise ValueError("Employee detail not found.")
            return employee
        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: ReadEmployees
    # Description:
    #   Retrieves a paginated list of employees.
    #   - Supports filtering, sorting, and pagination.
    # ------------------------------------------------------------
    def ReadEmployees(
        self,
        filter: str = '',
        order_by: str = 'id',
        order_direction: str = 'desc',
        limit: int = 10,
        page: int = 1
    ):
        try:
            if limit < 1:
                limit = 10
            if page < 1:
                page = 1

            data = employee_crud.read_employees(
                self.__db,
                filter,
                order_by,
                order_direction,
                limit,
                page
            )

            all_items = data["all_items"]
            employees = data["employees"]
            meta = {
                "current_item": len(employees),
                "limit": limit,
                "page": page,
                "total_items": all_items
            }

            return {
                "meta": meta,
                "employees": employees
            }
        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: DeleteEmployee
    # Description:
    #   Deletes an employee record by ID.
    #   - Only admins or the employee themselves can perform this.
    # ------------------------------------------------------------
    def DeleteEmployee(self, id: int):
        try:
            logged_in_employee = get_current_employee()
            if not logged_in_employee:
                raise PermissionError('Access denied')

            employee = employee_crud.get_employee_by_id(self.__db, id)
            if employee and (
                logged_in_employee.id == employee.id or
                logged_in_employee.employee_type == 'admin'
            ):
                self.__db.delete(employee)
                self.__db.commit()
                return "Employee deleted successfully."

            raise ValueError("Employee detail not found.")
        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: UpdateEmployee
    # Description:
    #   Updates an employee’s details.
    #   - Ensures permission: only admin or self.
    #   - Prevents duplicate emails.
    #   - Restricts non-admins from promoting themselves to admin.
    # ------------------------------------------------------------
    def UpdateEmployee(self, id: int, data):
        try:
            logged_in_employee = get_current_employee()
            if not logged_in_employee:
                raise PermissionError("Access denied")

            employee = employee_crud.get_employee_by_id(self.__db, id)
            if not employee:
                raise ValueError("Please provide valid details.")
            
            if logged_in_employee.employee_type != "admin" and employee.id != id:  # type: ignore
                raise PermissionError("Access denied")

            if hasattr(data, 'email') and data.email != '':
                employee_by_email = employee_crud.get_employee_by_email(self.__db, data.email)
                if employee_by_email and employee.id != employee_by_email.id:  # type: ignore
                    raise ValueError("Provided email already exists.")

            if hasattr(data, 'employee_type') and data.employee_type:
                if data.employee_type == 'admin' and logged_in_employee.employee_type == 'admin':
                    pass
                else:
                    data.employee_type = 'employee'

            employee = employee_crud.update_employee(self.__db, employee, data)
            return employee
        except Exception as e:
            raise ProcessLookupError(str(e))
