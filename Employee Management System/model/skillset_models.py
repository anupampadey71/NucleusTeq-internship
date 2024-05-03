from pydantic import BaseModel

class Register(BaseModel):
    skillId : str
    skillName : str 