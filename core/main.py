from fastapi import FastAPI, Query, status, HTTPException, Path
from typing import Annotated
from schemas import PersonCreateSchema, PersonResponsSchema, PersonUpdateSchema
from typing import List

names_list = [
    {"id": 1, "name": "amir", "age": 20},
    {"id": 2, "name": "shaqayeq", "age": 17},
    {"id": 3, "name": "ali", "age": 12},
    {"id": 4, "name": "danial", "age": 16},
    {"id": 5, "name": "aref", "age": 14},
]

app = FastAPI()


@app.get("/names/{name_id}", status_code=status.HTTP_200_OK, response_model=PersonResponsSchema)
async def retrive_name_detail(name_id: int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="obj not found")


@app.get("/names", status_code=status.HTTP_200_OK, response_model=List[PersonResponsSchema])
async def show_name_list(
    q: Annotated[
        str | None,
        Query(
            description="it will be searched with the title you provided",
            alias="Search",
            title="Search Name",
            examples="amir",
            max_length=20,
            min_length=3,
        ),
    ] = None,
):
    if not q:
        return names_list
    for item in names_list:
        if item["name"] == q:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="obj not found")


@app.put("/names/{name_id}", status_code=status.HTTP_200_OK, response_model=PersonResponsSchema)
async def update_name_detail(
    name_id: Annotated[
        int,
        Path(
            title="Name ID",
            ge=1,
            description="Enter id you want replace name",
            example=1,
        ),
    ], person: PersonUpdateSchema,
):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = person.name
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="obj not found")


@app.post("/names/{name_id}", status_code=status.HTTP_201_CREATED)
async def create_name(
    name_id: Annotated[
        int,
        Path(
            title="Name ID",
            ge=1,
            description="Enter id you want replace name",
            example=1,
        ),
    ],
    name: Annotated[
        str,
        Query(
            alias="Name",
            title="Name",
            description="Enter new name",
            min_length=3,
            max_length=20,
            example="amir",
        ),
    ],
):
    if any(item["id"] == name_id for item in names_list):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="ID already exists"
        )

    new_item = {"id": name_id, "name": name}
    names_list.append(new_item)
    return new_item


@app.delete("/names/{name_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_name_detail(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="obj not found")


@app.post("/names", status_code=status.HTTP_201_CREATED, response_model=List[PersonResponsSchema])
async def crate_res_name(person: PersonCreateSchema):
    name_obj = {'id': person.id, "name": person.name, "age": person.age}
    names_list.append(name_obj)
    return names_list
