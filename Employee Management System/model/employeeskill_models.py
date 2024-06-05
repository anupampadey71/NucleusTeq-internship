from pydantic import BaseModel, ValidationError, validator, constr

class Register(BaseModel):
    employeeId: constr(min_length=3, max_length=9)  # Constrained length for employeeId
    skillId: str

    @validator('employeeId')
    def validate_employee_id(cls, value):
        if not value.startswith('EMP'):
            raise ValueError('Employee ID must start with "EMP"')
        return value
