from pydantic import BaseModel

class Register(BaseModel):
    projectId : str
    name : str
    description : str
    managerId : str

class UpdateProject(BaseModel):
    name : str
    description : str
    managerId : str