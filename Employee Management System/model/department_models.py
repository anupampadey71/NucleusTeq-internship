from pydantic import BaseModel

class Register(BaseModel):
    departmentId : str
    name : str 
    managerId : str