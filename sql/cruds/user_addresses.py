from sqlalchemy.orm import Session
from sql.models.user_addresses import UserAddresses


def create_user_address(db: Session, user_id: int, address: dict):
    user_address = UserAddresses()
    user_address.user_id = user_id  # type: ignore
    user_address.address = address.get("address", "")
    user_address.city = address.get("city", "")
    user_address.state = address.get("state", "")
    user_address.zip_code = address.get("zip_code", "")
    user_address.is_default = address.get("is_default", False)
    db.add(user_address)
    db.commit()
    db.refresh(user_address)
    return user_address


def get_user_address_by_id(db: Session, address_id: int):
    return db.query(UserAddresses).filter(UserAddresses.id == address_id).first()


def get_user_addresses(db: Session, user_id: int):
    return db.query(UserAddresses).filter(UserAddresses.user_id == user_id).all()


def delete_user_address(db: Session, address_id: int):
    address = db.query(UserAddresses).filter(
        UserAddresses.id == address_id).first()
    if address:
        db.delete(address)
        db.commit()
    return address


def get_or_update_default_address(db: Session, user_id: int, is_default_changed: bool = False):
    address = db.query(UserAddresses).filter(
        UserAddresses.user_id == user_id, UserAddresses.is_default == True).first()

    if address and is_default_changed:
        address.is_default = bool(False) #type: ignore
        db.add(address)
        db.commit()
        db.refresh(address)
        return address
    return address
