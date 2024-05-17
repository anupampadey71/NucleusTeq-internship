from pydantic import BaseModel

class Register(BaseModel):
    assignmentId: str
    requestId: str
    employeeId: str
    projectId: str
    assigned: bool

class create_assignment(BaseModel):
    assignmentId: str
    requestId: str
    employeeId: str
    projectId: str
