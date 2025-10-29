from sqlalchemy.orm import Session
from sql.models.employee_addresses import employeeAddresses


# ------------------------------------------------------------
# Module: employee_address_crud
# Description:
#   Provides CRUD operations for managing employee address records.
#   Includes handling for default address management.
# ------------------------------------------------------------


# ------------------------------------------------------------
# Method: create_employee_address
# Description:
#   Creates and stores a new employee address record in the database.
#
# Parameters:
#   - db (Session): Active SQLAlchemy session.
#   - employee_id (int): Employee ID linked to this address.
#   - address (object): Object containing address fields.
#
# Returns:
#   - employeeAddresses: Newly created address record.
# ------------------------------------------------------------
def create_employee_address(db: Session, employee_id: int, address):
    employee_address = employeeAddresses()
    employee_address.employee_id = employee_id  # type: ignore
    employee_address.address = address.address
    employee_address.city = address.city
    employee_address.state = address.state
    employee_address.zip_code = address.zip_code
    employee_address.is_default = address.is_default

    db.add(employee_address)
    db.commit()
    db.refresh(employee_address)
    return employee_address


# ------------------------------------------------------------
# Method: get_employee_address_by_id
# Description:
#   Retrieves a specific address record by its ID.
# ------------------------------------------------------------
def get_employee_address_by_id(db: Session, address_id: int):
    return db.query(employeeAddresses).filter(employeeAddresses.id == address_id).first()


# ------------------------------------------------------------
# Method: get_employee_addresses
# Description:
#   Retrieves all address records for a specific employee.
# ------------------------------------------------------------
def get_employee_addresses(db: Session, employee_id: int):
    return db.query(employeeAddresses).filter(employeeAddresses.employee_id == employee_id).all()


# ------------------------------------------------------------
# Method: delete_employee_address
# Description:
#   Deletes an employee address record based on the given ID.
#   Returns the deleted record if found, else None.
# ------------------------------------------------------------
def delete_employee_address(db: Session, address_id: int):
    address = db.query(employeeAddresses).filter(
        employeeAddresses.id == address_id
    ).first()
    if address:
        db.delete(address)
        db.commit()
    return address


# ------------------------------------------------------------
# Method: get_or_update_default_address
# Description:
#   Retrieves or updates the default address for an employee.
#   - If `is_default_changed` is True, unsets the existing default address.
#
# Parameters:
#   - db (Session): SQLAlchemy database session.
#   - employee_id (int): Employee ID whose default address is checked/updated.
#   - is_default_changed (bool): Flag indicating if default should be reset.
#
# Returns:
#   - employeeAddresses | None: The found or updated default address.
# ------------------------------------------------------------
def get_or_update_default_address(db: Session, employee_id: int, is_default_changed: bool = False):
    address = db.query(employeeAddresses).filter(
        employeeAddresses.employee_id == employee_id,
        employeeAddresses.is_default == True
    ).first()

    if address and is_default_changed:
        address.is_default = False  # type: ignore
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    return address
