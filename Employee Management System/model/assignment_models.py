from pydantic import BaseModel

class Register(BaseModel):
    assignmentId: str
    requestId: str
    employeeId: str
    projectId: str
    status: str
