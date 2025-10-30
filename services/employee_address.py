import db
from sql.cruds import employee_addresses as employee_address_crud
from decouple import config
from dotenv import load_dotenv
from middleware.auth_middleware import get_current_employee

# ------------------------------------------------------------
# Service: EmployeeAddressService
# Description:
#   Handles CRUD operations for employee addresses.
#   Includes access control to ensure employees can only
#   modify their own addresses unless they are admin.
# ------------------------------------------------------------

load_dotenv()


class EmployeeAddressService:
    # ------------------------------------------------------------
    # Constructor
    # Initializes database connection.
    # ------------------------------------------------------------
    def __init__(self):
        self.__db = db.get_db()

    # ------------------------------------------------------------
    # Method: create_employee_address
    # Description:
    #   Creates a new address record for an employee.
    #   - Verifies user authentication.
    #   - Updates existing default address if necessary.
    # ------------------------------------------------------------
    def create_employee_address(self, employee_id, data):
        try:
            logged_in_employee = get_current_employee()
            if not logged_in_employee:
                raise PermissionError("Access Denied")

            if data.is_default is True:
                employee_address_crud.get_or_update_default_address(
                    self.__db, employee_id, True
                )

            employee_address_crud.create_employee_address(self.__db, employee_id, data)
            return "Address Created Successfully"

        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: delete_employee_address
    # Description:
    #   Deletes an existing employee address by ID.
    #   - Prevents deletion of default address.
    #   - Restricts access to admin or the owner employee.
    # ------------------------------------------------------------
    def delete_employee_address(self, address_id):
        try:
            logged_in_employee = get_current_employee()
            if not logged_in_employee:
                raise PermissionError("Access Denied")

            address = employee_address_crud.get_employee_address_by_id(
                self.__db, address_id
            )

            if not address:
                raise ValueError("Address Not Found")

            if address.is_default:  # type: ignore
                raise ValueError("Default Address cannot be deleted")

            if (
                logged_in_employee.employee_type != 'admin'
                and logged_in_employee.id != address.employee_id
            ):
                raise PermissionError("Access Denied")

            employee_address_crud.delete_employee_address(self.__db, address_id)
            return "Address Deleted Successfully"

        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: read_employee_addresses
    # Description:
    #   Retrieves all addresses for a specific employee.
    #   - Restricts access to admin or the employee themselves.
    # ------------------------------------------------------------
    def read_employee_addresses(self, employee_id: int):
        try:
            logged_in_employee = get_current_employee()
            if not logged_in_employee:
                raise PermissionError("Access Denied")

            if (
                logged_in_employee.employee_type != "admin"
                and logged_in_employee.id != employee_id
            ):
                raise PermissionError("Access Denied.")

            address = employee_address_crud.get_employee_addresses(
                self.__db, employee_id
            )
            return {"address": address}

        except Exception as e:
            raise ProcessLookupError(str(e))
