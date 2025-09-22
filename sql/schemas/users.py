from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from sql.models.users import User as UserModel


class LoggedInUserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        include_relationships = True
        include_fk = True
        fields = (
            "id",
            "email",
            "name",
            "user_type",
        )


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        include_relationships = True
        include_fk = True
        fields = (
            "id",
            "name",
            "email",
            "password",
            "user_type",
            "created_at",
            "updated_at",
            "addresses",
        )
    # user = Nested(UserContactSchema())


class CreateUserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        include_relationships = True
        include_fk = True
        fields = (
            "name",
            "email",
            "password",
        )


class ReadAllUser(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        include_relationships = True
        include_fk = True
        fields = (

            "id",
            "name",
            "email",
            "password",
            "user_type",
            "created_at",
            "updated_at",
            "addresses",
        )
    # user = Nested(UserContactSchema())
