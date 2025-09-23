from sql.models.users import User
from sqlalchemy.orm import Session
import bcrypt
from sqlalchemy import and_, asc, desc, or_


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data) -> User:
    user = User()
    user.name = user_data.name
    user.email = user_data.email
    user.password = _encoded_password(user_data.password)  # type: ignore
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _encoded_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes(password, "utf-8"), salt)


def _check_password(password, hashed_password) -> bool:
    h_password = bytes(hashed_password, "utf-8")
    _password = bytes(password, "utf-8")
    return bcrypt.checkpw(_password, h_password)


def read_users(
    db: Session,
    filter: str = '',
    order_by: str = 'id',
    order_direction: str = 'desc',
    limit: int = 10,
    page: int = 1
):
    query = (db.query(User)
            #  .filter(and_(User.user_type != 'admin'))
             )  # type: ignore

    if filter and filter != "":
        filter_data = "%{}%".format(filter.strip())
        query = query.filter(
            or_(
                User.id.like(filter_data),
                User.name.like(filter_data),
                User.email.like(filter_data),
            )

        )

    if order_by and order_by != "":
        dicrection = desc if order_direction == 'desc' else asc
        query = query.order_by(dicrection(getattr(User, order_by)))

    all = query.count()

    if limit and limit > 0:
        query = query.limit(limit)
        offset = (int(page) - 1) * limit
        query = query.offset(offset)

    users = query.all()
    return {
        "all_items": all,
        "users": users
    }


def update_user(db: Session, user: User, new_user):
    if hasattr(new_user, 'name') and new_user.name != '':
        user.name = new_user.name

    if hasattr(new_user, 'email') and new_user.email:
        user.email = new_user.email

    if hasattr(new_user, 'password') and new_user.password:
        user.password = _encoded_password(new_user.password)

    if hasattr(new_user, 'user_type') and new_user.user_type:
        user.user_type = new_user.user_type

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
