import re
from pydantic import BaseModel, Field, validator

class EmployeeIdPattern:
    """Custom class to define employee ID pattern."""
    pattern = r"^(ADM|EMP|MGR)[0-9]+$"


class Register(BaseModel):
    """Employee model with validations."""

    employeeId: str
    email: str
    name: str
    salary: int
    role: str

    @validator('employeeId')
    def validate_employeeId(cls, value):
        """Validates employeeId pattern."""
        if not re.match(EmployeeIdPattern.pattern, value):
            raise ValueError("Invalid employeeId prefix")
        return value

    @validator('email')
    def validate_email(cls, value):
        """Ensures email ends with @company.com."""
        if not value.endswith("@company.com"):
            raise ValueError("Email must end with @company.com")
        return value

class UpdateEmployeeDetails(BaseModel):
    """Model for updating employee details (optional fields)."""

    email: str
    name: str
    salary: int
    role: str 
    is_assigned: bool 

    @validator('email')
    def validate_update_email(cls, value):
        """Validates email if provided during update."""
        if value and not value.endswith("@company.com"):
            raise ValueError("Email must end with @company.com")
        return value
