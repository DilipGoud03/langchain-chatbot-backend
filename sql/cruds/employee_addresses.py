from sqlalchemy.orm import Session
from sql.models.employee_addresses import employeeAddresses


def create_employee_address(db: Session, employee_id: int, address):
    print('====Here====1')
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


def get_employee_address_by_id(db: Session, address_id: int):
    return db.query(employeeAddresses).filter(employeeAddresses.id == address_id).first()


def get_employee_addresses(db: Session, employee_id: int):
    return db.query(employeeAddresses).filter(employeeAddresses.employee_id == employee_id).all()


def delete_employee_address(db: Session, address_id: int):
    address = db.query(employeeAddresses).filter(
        employeeAddresses.id == address_id).first()
    if address:
        db.delete(address)
        db.commit()
    return address


def get_or_update_default_address(db: Session, employee_id: int, is_default_changed: bool = False):
    address = db.query(employeeAddresses).filter(
        employeeAddresses.employee_id == employee_id, employeeAddresses.is_default == True).first()

    if address and is_default_changed:
        address.is_default = bool(False) #type: ignore
        db.add(address)
        db.commit()
        db.refresh(address)
        return address
    return address
