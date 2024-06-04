from pydantic import BaseModel, constr, ValidationError, validator

class Register(BaseModel):
    projectId: constr(min_length=5, max_length=9)
    name: str
    description: str
    managerId: constr(min_length=5, max_length=9)

    @validator('projectId')
    def validate_project_id(cls, value):
        if not value.startswith('PROJ'):
            raise ValueError('Project ID must start with "PROJ"')
        return value

    @validator('managerId')
    def validate_manager_id(cls, value):
        if not value.startswith('MGR'):
            raise ValueError('Manager ID must start with "MGR"')
        return value

class UpdateProject(BaseModel):
    name: str 
    description: str
    managerId: constr(min_length=5, max_length=9)

    @validator('managerId')
    def validate_manager_id(cls, value):
        if value and not value.startswith('MGR'):
            raise ValueError('Manager ID must start with "MGR" if provided')
        return value