from pydantic import BaseModel

class Register(BaseModel):
    managerId : str
    employeeId : str