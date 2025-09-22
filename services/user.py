import db
from sql.cruds import users as user_crud
import jwt
from datetime import datetime, timedelta
from decouple import config
from dotenv import load_dotenv
from middleware.auth_middleware import get_current_user

load_dotenv()


class UserService:
    def __init__(self):
        self.__db = db.get_db()

    def CreateUser(self, user_data):
        try:
            user = user_crud.get_user_by_email(self.__db, user_data.email)
            if user:
                raise ValueError("Please use diffrent email address.")
            user_crud.create_user(self.__db, user_data)
            return "User has created a successfuly"
        except Exception as e:
            raise LookupError(str(e))

    def LoginUser(self, user_data):
        try:
            user_name = user_data.email
            password = user_data.password
            user = user_crud.get_user_by_email(self.__db, user_name)
            token = None
            if user:
                if user_crud._check_password(password, user.password):
                    token = jwt.encode(
                        {
                            "exp": datetime.utcnow() + timedelta(days=1),
                            "iat": datetime.utcnow(),
                            "email": user.email,
                            "id": user.id,
                        },
                        str(config("SECRET_KEY")),
                        str(config("ALGORITHM"))
                    )
            if token is None:
                raise ValueError("Invalid username or password")
            return token
        except Exception as e:
            raise ProcessLookupError(str(e))

    def GetCurrentUser(self):
        try:
            user = get_current_user()
            return user
        except Exception as e:
            raise ProcessLookupError(str(e))

    def ReadUser(self, id: int):
        try:
            user = user_crud.get_user_by_id(self.__db, id)
            if not user:
                raise ValueError("User detail not found.")
            return user
        except Exception as e:
            raise ProcessLookupError(str(e))

    def ReadUsers(self,
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

            data = user_crud.read_users(
                self.__db,
                filter,
                order_by,
                order_direction,
                limit,
                page
            )

            all = data["all_items"]
            users = data["users"]
            meta = {
                "current_item": len(users),
                "limit": limit,
                "page": page,
                "total_items": all
            }
            return {
                "meta": meta,
                "users": users
            }

        except Exception as e:
            raise ProcessLookupError(str(e))

    def DeleteUser(self, id: int):
        try:
            logged_in_user = get_current_user()
            if not logged_in_user:
                raise PermissionError('Access denied')

            user = user_crud.get_user_by_id(self.__db, id)
            if user and (logged_in_user.id == user.id or logged_in_user.user_type == 'admin'):
                self.__db.delete(user)
                self.__db.commit()
                return "User deleted successfuly."
            raise ValueError("User detail not found.")
        except Exception as e:
            raise ProcessLookupError(str(e))

    def UpdateUser(self, id: int, data):
        try:
            logged_in_user = get_current_user()
            if not logged_in_user:
                raise PermissionError("Access denied")

            user = user_crud.get_user_by_id(self.__db, id)
            if not user:
                raise ValueError("Please provide the valid details")
            
            if logged_in_user.user_type != "admin" and user.id != id:  # type: ignore
                raise PermissionError("Access denied")

            
            if hasattr(data, 'email') and data.email != '':
                user_by_email = user_crud.get_user_by_email(self.__db, data.email)
                if user_by_email and user.id != user_by_email.id:  # type: ignore
                    raise ValueError("Provided email already exist.")

            if hasattr(data, 'user_type') and data.user_type:
                if data.user_type == 'admin' and logged_in_user.user_type == 'admin':
                    pass
                else:
                    data.user_type = 'employee'

            user = user_crud.update_user(self.__db, user, data)
            return user
        except Exception as e:
            raise ProcessLookupError(str(e))
