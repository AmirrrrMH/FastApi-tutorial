from pydantic import BaseModel, field_serializer, field_validator, Field
from typing import Annotated, Optional


class ResponsPersonModel(BaseModel):
    id: int
    description: str
    amount: int


class BasePersonSchema(BaseModel):
    id: int = Field(..., gt=0, alias="ID", description="Enter Your ID: ")

    @field_validator("id", mode="before")
    @classmethod
    def prevent_string_id(cls, v):
        if v is None:
            raise ValueError("ID is requierd")
        if isinstance(v, str):
            if not v.strip():
                raise ValueError("ID Cannot be None")
            if not v.isdigit():
                raise ValueError("ID must be integer")
        return v

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class CreatePersonSchema(BasePersonSchema):
    descript: Optional[Annotated[str, Field(
        min_length=3, alias="Description", max_length=20)]] = None
    amount: Annotated[int, Field(
        ge=0, alias="Cost", description="must be integer")]


class UpdatePersonSchema(BaseModel):
    id: int = Field(..., gt=0, alias="ID")
    descript: Optional[str] = Field(
        None, min_length=3, max_length=20, alias="Description")
    amount: Optional[int] = Field(None, ge=0, alias="Cost")
