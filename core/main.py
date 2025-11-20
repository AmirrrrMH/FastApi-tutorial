from fastapi import FastAPI

names_list = [
    {"id": 1, "name": "amir"},
    {"id": 2, "name": "shaqayeq"},
    {"id": 3, "name": "ali"},
    {"id": 4, "name": "danial"},
    {"id": 5, "name": "aref"},
]

app = FastAPI()


@app.get("/names/{name_id}")
async def retrive_name_detail(name_id: int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    return {"detail": "not found eror"}


@app.get("/names")
async def show_name_list():
    return names_list


@app.put("/names/{name_id}")
async def update_name_detail(name_id: int, name: str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    return {"detail": "not found eror"}


@app.post("/names/{name_id}")
async def create_name(name_id: int, name: str):
    name = {"id": name_id, "name": name}
    for item in names_list:
        if name_id != item["id"]:
            names_list.append(name)
            return name
        else:
            return {"detail": "id exist"}


@app.delete("/names/{name_id}")
async def delete_name_detail(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return {"detail": "delete object"}
    return {"detail": "not found eror"}
