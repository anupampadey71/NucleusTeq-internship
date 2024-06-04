from pydantic import BaseModel, ValidationError, validator, constr

class Register(BaseModel):
    departmentId: constr(min_length=5, max_length=9)
    name: str
    managerId: constr(min_length=5, max_length=9)

    @validator('departmentId')
    def validate_department_id(cls, value):
        if not value.startswith('DEPT'):
            raise ValueError('Department ID must start with "DEPT"')
        return value

    @validator('managerId')
    def validate_manager_id(cls, value):
        if not value.startswith('MGR'):
            raise ValueError('Manager ID must start with "MGR"')
        return value
