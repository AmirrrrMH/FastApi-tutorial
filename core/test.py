from fastapi import FastAPI, Path, HTTPException, status, Query
from typing import Annotated


app = FastAPI()

db_price = [
    {"id": 1, "description": "test1", "amount": 10.00},
    {"id": 2, "description": "test2", "amount": 20.00},
    {"id": 3, "description": "test3", "amount": 30.00},
    {"id": 4, "description": "test4", "amount": 40.00},
    {"id": 6, "description": "test6", "amount": 50.00},
]


@app.get("/CostManagement")
async def get_all_cost(
    name_id: Annotated[int | None, Query(alias="Name ID")] = None,
):
    if not name_id:
        return db_price
    for item in db_price:
        if item["id"] == name_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="obj not found")


@app.post("/CostManagement/{name_id}", status_code=status.HTTP_201_CREATED)
async def create_cost(
    name_id: Annotated[
        int,
        Path(
            title="Name ID",
            ge=1,
        ),
    ],
    description: Annotated[
        str, Query(alias="Description", min_length=5, max_length=50)
    ],
    cost: Annotated[
        float,
        Query(
            alias="Cost",
            description="Cost amount as a decimal number",
            example=11.23,
            ge=1,
        ),
    ],
):
    if any(item["id"] == name_id for item in db_price):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="ID already exists"
        )

    new_cost = {"id": name_id, "description": description, "amount": cost}
    db_price.append(new_cost)
    return new_cost


@app.put("/CostManagement/{name_id}")
async def update_cost(
    name_id: Annotated[int, Path(title="Name ID", ge=1)],
    description: Annotated[str, Query(alias="description", min_length=3)],
    cost: Annotated[
        float,
        Query(
            alias="Cost",
            description="Cost amount as a decimal number",
            example=11.23,
            ge=1,
        ),
    ],
):
    for item in db_price:
        if item["id"] == name_id:
            item["description"] = description
            item["amount"] = cost
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="obj not found")


@app.delete("/CostManagement/{name_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delet_cost(name_id: Annotated[int, Path(title="Name ID", ge=1)]):
    for item in db_price:
        if item["id"] == name_id:
            return db_price.remove(item)
