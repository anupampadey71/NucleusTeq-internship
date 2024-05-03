from pydantic import BaseModel

class Register(BaseModel):
    projectId : str
    name : str
    description : str