from sql.models.employees import Employee
from sqlalchemy.orm import Session
import bcrypt
from sqlalchemy import asc, desc, or_


# ------------------------------------------------------------
# Module: employee_crud
# Description:
#   Provides CRUD operations for managing employee records.
#   Includes helpers for password hashing, filtering, and pagination.
# ------------------------------------------------------------


# ------------------------------------------------------------
# Method: get_employee_by_id
# Description:
#   Retrieves an employee record using the employee ID.
# ------------------------------------------------------------
def get_employee_by_id(db: Session, employee_id: int) -> Employee:
    return db.query(Employee).filter(Employee.id == employee_id).first()


# ------------------------------------------------------------
# Method: get_employee_by_email
# Description:
#   Fetches an employee record by their email address.
# ------------------------------------------------------------
def get_employee_by_email(db: Session, email: str) -> Employee:
    return db.query(Employee).filter(Employee.email == email).first()


# ------------------------------------------------------------
# Method: create_employee
# Description:
#   Creates a new employee record in the database.
#   - Hashes the password before saving.
# ------------------------------------------------------------
def create_employee(db: Session, employee_data) -> Employee:
    employee = Employee()
    employee.name = employee_data.name
    employee.email = employee_data.email
    employee.password = _encoded_password(employee_data.password)  # type: ignore

    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


# ------------------------------------------------------------
# Method: _encoded_password
# Description:
#   Hashes a plain-text password using bcrypt with salt.
# ------------------------------------------------------------
def _encoded_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


# ------------------------------------------------------------
# Method: _check_password
# Description:
#   Verifies if a plain-text password matches a hashed one.
# ------------------------------------------------------------
def _check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# ------------------------------------------------------------
# Method: read_employees
# Description:
#   Retrieves a paginated list of employees with optional filters and sorting.
#
# Parameters:
#   - filter (str): Search keyword for employee ID, name, or email.
#   - order_by (str): Column name to order results by (default: 'id').
#   - order_direction (str): Sort order, 'asc' or 'desc' (default: 'desc').
#   - limit (int): Number of records per page (default: 10).
#   - page (int): Page number (default: 1).
#
# Returns:
#   - dict: Contains employee list and pagination metadata.
# ------------------------------------------------------------
def read_employees(
    db: Session,
    filter: str = '',
    order_by: str = 'id',
    order_direction: str = 'desc',
    limit: int = 10,
    page: int = 1
):
    query = db.query(Employee)

    # Apply text-based filters
    if filter:
        filter_data = f"%{filter.strip()}%"
        query = query.filter(
            or_(
                Employee.id.like(filter_data),
                Employee.name.like(filter_data),
                Employee.email.like(filter_data),
            )
        )

    # Sorting
    if order_by:
        direction = desc if order_direction == 'desc' else asc
        query = query.order_by(direction(getattr(Employee, order_by)))

    # Count before pagination
    total_items = query.count()

    # Pagination
    if limit > 0:
        offset = (page - 1) * limit
        query = query.limit(limit).offset(offset)

    employees = query.all()

    return {
        "all_items": total_items,
        "employees": employees
    }


# ------------------------------------------------------------
# Method: update_employee
# Description:
#   Updates an employee record with new data fields.
#   - Supports partial updates (only non-empty fields are applied).
# ------------------------------------------------------------
def update_employee(db: Session, employee: Employee, new_employee):
    if hasattr(new_employee, 'name') and new_employee.name:
        employee.name = new_employee.name

    if hasattr(new_employee, 'email') and new_employee.email:
        employee.email = new_employee.email

    if hasattr(new_employee, 'password') and new_employee.password:
        employee.password = _encoded_password(new_employee.password)

    if hasattr(new_employee, 'employee_type') and new_employee.employee_type:
        employee.employee_type = new_employee.employee_type

    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
