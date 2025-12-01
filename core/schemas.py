from pydantic import BaseModel, Field, field_validator, field_serializer


class BasePersonSchema(BaseModel):
    name: str = Field(..., description="Persons name: ")
    age: int = Field(..., description="Persons age: ")

    @field_validator("name")
    def name_validator(cls, value):
        if value == "" or value is None:
            raise ValueError("name cannot be empty")
        return value

    @field_validator('age')
    def age_validator(cls, value):
        if value <= 0:
            raise ValueError("Your age must be more than 0")
        return value

    @field_serializer('name')
    def upper_name(self, value):
        return value.title()


class PersonCreateSchema(BasePersonSchema):
    id: int


class PersonResponsSchema(BasePersonSchema):
    id: int

    class Config:
        from_attributes = True


class PersonUpdateSchema(BasePersonSchema):
    pass
