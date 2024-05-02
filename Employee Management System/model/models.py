from pydantic import BaseModel

class Register(BaseModel):
    employeeId : str
    email : str
    name : str 
    salary : str
    role : str
    