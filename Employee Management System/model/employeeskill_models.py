from pydantic import BaseModel

class Register(BaseModel):
    employeeId: str
    skillId : str 