from pydantic import BaseModel
from enum import Enum

class StatusEnum(str, Enum):
    open = "Open"
    close = "Close"

class Register(BaseModel):
    requestId : str
    projectId : str
    skillId : str
    status : StatusEnum



class UpdateRequestModel(BaseModel):
    status: StatusEnum