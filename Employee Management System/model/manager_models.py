from pydantic import BaseModel, constr, validator

class Register(BaseModel):
    managerId: constr(min_length=5, max_length=9)
    employeeId: constr(min_length=5, max_length=9)

    @validator('managerId')
    def validate_manager_id(cls, value):
        if not value.startswith('MGR'):
            raise ValueError('Manager ID must start with "MGR"')
        return value

    @validator('employeeId')
    def validate_employee_id(cls, value):
        if not value.startswith('EMP'):
            raise ValueError('Employee ID must start with "EMP"')
        return value
