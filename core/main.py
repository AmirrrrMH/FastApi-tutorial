from fastapi import FastAPI, Query, status, HTTPException
from typing import Annotated

names_list = [
    {"id": 1, "name": "amir"},
    {"id": 2, "name": "shaqayeq"},
    {"id": 3, "name": "ali"},
    {"id": 4, "name": "danial"},
    {"id": 5, "name": "aref"},
]

app = FastAPI()


@app.get("/names/{name_id}", status_code=status.HTTP_200_OK)
async def retrive_name_detail(name_id: int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="obj not found")


@app.get("/names")
async def show_name_list(q: Annotated[str | None, Query(max_length=20)] = None):
    if q:
        return [item for item in names_list if item["name"] == q]
    return names_list


@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
async def update_name_detail(name_id: int, name: str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="obj not found")


@app.post("/names/{name_id}", status_code=status.HTTP_201_CREATED)
async def create_name(name_id: int, name: str):
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
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="obj not found")
