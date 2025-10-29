from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from sql.models.employees import Employee as EmployeeModel


# ------------------------------------------------------------
# Schema: LoggedInEmployeeSchema
# Description:
#   Defines the serialized structure for a logged-in employee.
#
#   Used for responses after authentication or profile retrieval,
#   excluding sensitive information like passwords.
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# Schema: EmployeeSchema
# Description:
#   Provides full serialization for employee data, including
#   related addresses and metadata such as creation and update timestamps.
#
#   This schema is typically used for admin views or internal API responses.
# ------------------------------------------------------------
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
    # addresses = Nested(employeeAddressSchema())  # Example for nested relation


# ------------------------------------------------------------
# Schema: CreateEmployeeSchema
# Description:
#   Defines the structure for creating a new employee record.
#
#   Used when registering or adding new employees; excludes
#   read-only fields such as timestamps or relationships.
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# Schema: ReadAllEmployeeSchema
# Description:
#   Defines the structure for reading all employee records.
#
#   Includes address relationships and all standard employee
#   attributes for administrative listing and reporting.
# ------------------------------------------------------------
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
    # addresses = Nested(employeeAddressSchema())  # Optional nested relationship
