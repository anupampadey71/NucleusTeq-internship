from pydantic import BaseModel

class Register(BaseModel):
    requestId : str
    projectId : str
    skillId : str
    status : str