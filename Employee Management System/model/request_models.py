from pydantic import BaseModel, ValidationError, validator, constr
from enum import Enum

class StatusEnum(str, Enum):
    open = "Open"
    close = "Close"

class Register(BaseModel):
    requestId: constr(min_length=3, max_length=9)  # Constrained length for requestId
    projectId: str
    skillId: str
    status: StatusEnum

    @validator('requestId')
    def validate_request_id(cls, value):
        if not value.startswith('REQ'):
            raise ValueError('Request ID must start with "REQ"')
        return value


class UpdateRequestModel(BaseModel):
    status: StatusEnum
