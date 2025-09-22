import db
from sql.cruds import user_addresses as user_address_crud
import jwt
from datetime import datetime, timedelta
from decouple import config
from dotenv import load_dotenv
from middleware.auth_middleware import get_current_user

load_dotenv()


class UserAddressService:
    def __init__(self):
        self.__db = db.get_db()

    def CreateNewAddress(self, user_id, data):
        try:
            logged_in_user = get_current_user()
            if not logged_in_user:
                raise PermissionError("Access Denied")
            if data.is_default is True:
                user_address_crud.get_or_update_default_address(
                    self.__db, user_id, True)
            user_address_crud.create_user_address(self.__db, user_id, data)
            return "Address Created Successfully"
        except Exception as e:
            raise ProcessLookupError(str(e))

    def DeleteUserAddress(self, address_id):
        try:
            logged_in_user = get_current_user()
            if not logged_in_user:
                raise PermissionError("Access Denied")
            address = user_address_crud.get_user_address_by_id(
                self.__db, address_id)
            if not address:
                raise ValueError("Address Not Found")
            if address.is_default:  # type: ignore
                raise ValueError("Default Address cannot be deleted")

            if logged_in_user.user_type != 'admin' and logged_in_user.id != address.user_id:
                raise PermissionError("Access Denied")

            user_address_crud.delete_user_address(self.__db, address_id)
            return "Address Deleted Successfully"
        except Exception as e:
            raise ProcessLookupError(str(e))

    def ReadUserAdrresses(self, user_id: int):
        try:
            logged_in_user = get_current_user()
            if not logged_in_user:
                raise PermissionError("Access Denied")

            if logged_in_user.user_type != "admin" and logged_in_user.id != user_id:
                raise PermissionError("Access Denied.")
            address = user_address_crud.get_user_addresses(self.__db, user_id)
            return {"address": address}
        except Exception as e:
            raise ProcessLookupError(str(e))
