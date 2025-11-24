from pydantic import BaseModel


class PersonCreateSchema(BaseModel):
    id: int
    name: str
    age: int


class PersonResponsSchema(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True
