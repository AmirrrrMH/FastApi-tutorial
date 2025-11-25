from pydantic import BaseModel, field_validator


class BasePersonSchema(BaseModel):
    name: str
    age: int

    @field_validator("name")
    def name_validator(cls, value):
        if value == "" or value is None:
            raise ValueError("name cannot be empty")

    @field_validator('age')
    def age_validator(cls, value):
        if value <= 0:
            raise ValueError("Your age must be more than 0")
        return value


class PersonCreateSchema(BasePersonSchema):
    id: int


class PersonResponsSchema(BasePersonSchema):
    id: int

    class Config:
        from_attributes = True


class PersonUpdateSchema(BasePersonSchema):
    pass
