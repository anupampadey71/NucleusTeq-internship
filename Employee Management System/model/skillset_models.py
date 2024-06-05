from pydantic import BaseModel, ValidationError, validator, constr

class Register(BaseModel):
    skillId: constr(min_length=5, max_length=9)
    skillName: str

    @validator('skillId')
    def validate_skill_id(cls, value):
        if not value.startswith('SKILL'):
            raise ValueError('Skill ID must start with "SKILL"')
        return value
