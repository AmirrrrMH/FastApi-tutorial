from fastapi import FastAPI, Path, HTTPException, status, Query
from typing import List, Optional
from schemas_test import BasePersonSchema, CreatePersonSchema, UpdatePersonSchema, ResponsPersonModel

app = FastAPI(title="Cost Management API")


db: List[dict] = [
    {"id": 1, "description": "test1", "amount": 10},
    {"id": 2, "description": "test2", "amount": 20},
    {"id": 3, "description": "test3", "amount": 30},
    {"id": 4, "description": "test4", "amount": 40},
    {"id": 6, "description": "test6", "amount": 50},
]


@app.get("/cost-management", response_model=list[ResponsPersonModel])
async def get_all_items(id: Optional[int] = Query(None, alias="ID")):
    if id is not None:
        filtered = [item for item in db if item["id"] == id]
        if not filtered:
            raise HTTPException(status_code=404, detail="Item not found")
        return filtered

    return db


@app.post("/cost-management", status_code=status.HTTP_201_CREATED, response_model=ResponsPersonModel)
async def create_item(item: CreatePersonSchema):
    if any(existing["id"] == item.id for existing in db):
        raise HTTPException(
            status_code=409, detail="Item with this ID already exists")

    new_item = {
        "id": item.id,
        "description": item.descript or "",
        "amount": item.amount or 0
    }
    db.append(new_item)
    return new_item


@app.put("/cost-management/{item_id}", response_model=BasePersonSchema)
async def update_item(
    item_id: int = Path(..., ge=1, description="ID of the item to update"),
    payload: UpdatePersonSchema = None
):
    if payload.id != item_id:
        raise HTTPException(
            status_code=400, detail="ID in path and body must match")

    for item in db:
        if item["id"] == item_id:
            if payload.descript is not None:
                item["description"] = payload.descript
            if payload.amount is not None:
                item["amount"] = payload.amount
            return item

    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/cost-management/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int = Path(..., ge=1)):
    for item in db:
        if item["id"] == item_id:
            db.remove(item)
            return None
    raise HTTPException(status_code=404, detail="Item not found")
