from pydantic import BaseModel, ValidationError, validator, constr




class create_assignment(BaseModel):
    assignmentId: constr(min_length=4, max_length=9)  # Constrained length for assignmentId
    requestId: str
    employeeId: str
    projectId: str

    @validator('assignmentId')
    def validate_assignment_id(cls, value):
        if not value.startswith('ASSG'):
            raise ValueError('Assignment ID must start with "ASSG"')
        return value
