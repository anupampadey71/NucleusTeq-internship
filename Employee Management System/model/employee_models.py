from pydantic import BaseModel

class Register(BaseModel):
    employeeId: str
    email: str
    name: str
    salary: int
    role: str



class UpdateEmployeeDetails(BaseModel):
    email: str
    name: str
    salary: int
    role: str
    is_assigned: bool
