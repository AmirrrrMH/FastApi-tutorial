from pydantic import BaseModel


class BasePersonSchema(BaseModel):
    pass


class PersonCreateSchema(BasePersonSchema):
    id: int
    age: int


class PersonResponsSchema(BasePersonSchema):
    id: int

    class Config:
        from_attributes = True


class PersonUpdateSchema(BasePersonSchema):
    pass
