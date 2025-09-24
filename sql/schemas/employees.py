from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from sql.models.employees import Employee as EmployeeModel


class LoggedInEmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeModel
        load_instance = True
        include_relationships = True
        include_fk = True
        fields = (
            "id",
            "email",
            "name",
            "employee_type",
        )


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeModel
        load_instance = True
        include_relationships = True
        include_fk = True
        fields = (
            "id",
            "name",
            "email",
            "password",
            "employee_type",
            "created_at",
            "updated_at",
            "addresses",
        )
    # employee = Nested(employeeContactSchema())


class CreateEmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeModel
        load_instance = True
        include_relationships = True
        include_fk = True
        fields = (
            "name",
            "email",
            "password",
        )


class ReadAllEmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeModel
        load_instance = True
        include_relationships = True
        include_fk = True
        fields = (

            "id",
            "name",
            "email",
            "password",
            "employee_type",
            "created_at",
            "updated_at",
            "addresses",
        )
    # employee = Nested(employeeContactSchema())
