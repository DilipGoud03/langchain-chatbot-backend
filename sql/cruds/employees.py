from sql.models.employees import Employee
from sqlalchemy.orm import Session
import bcrypt
from sqlalchemy import and_, asc, desc, or_


def get_employee_by_id(db: Session, employee_id: int) -> Employee:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employee_by_email(db: Session, email: str) -> Employee:
    return db.query(Employee).filter(Employee.email == email).first()


def create_employee(db: Session, employee_data) -> Employee:
    employee = Employee()
    employee.name = employee_data.name
    employee.email = employee_data.email
    employee.password = _encoded_password(employee_data.password)  # type: ignore
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def _encoded_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes(password, "utf-8"), salt)


def _check_password(password, hashed_password) -> bool:
    h_password = bytes(hashed_password, "utf-8")
    _password = bytes(password, "utf-8")
    return bcrypt.checkpw(_password, h_password)


def read_employees(
    db: Session,
    filter: str = '',
    order_by: str = 'id',
    order_direction: str = 'desc',
    limit: int = 10,
    page: int = 1
):
    query = (db.query(Employee)
            #  .filter(and_(Employee.employee_type != 'admin'))
             )  # type: ignore

    if filter and filter != "":
        filter_data = "%{}%".format(filter.strip())
        query = query.filter(
            or_(
                Employee.id.like(filter_data),
                Employee.name.like(filter_data),
                Employee.email.like(filter_data),
            )

        )

    if order_by and order_by != "":
        dicrection = desc if order_direction == 'desc' else asc
        query = query.order_by(dicrection(getattr(Employee, order_by)))

    all = query.count()

    if limit and limit > 0:
        query = query.limit(limit)
        offset = (int(page) - 1) * limit
        query = query.offset(offset)

    employees = query.all()
    return {
        "all_items": all,
        "employees": employees
    }


def update_employee(db: Session, employee: Employee, new_employee):
    if hasattr(new_employee, 'name') and new_employee.name != '':
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
