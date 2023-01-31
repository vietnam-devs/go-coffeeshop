from decimal import *
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    type: int
    price: Decimal


items = {
    "CAPPUCCINO": Item(name="CAPPUCCINO", type=0, price=4.5),
    "COFFEE_BLACK": Item(name="COFFEE_BLACK", type=1, price=3),
    "COFFEE_WITH_ROOM": Item(name="COFFEE_WITH_ROOM", type=2, price=3),
    "ESPRESSO": Item(name="ESPRESSO", type=3, price=3.5),
    "ESPRESSO_DOUBLE": Item(name="ESPRESSO_DOUBLE", type=4, price=4.5),
    "LATTE": Item(name="LATTE", type=5, price=4.5),
    "CAKEPOP": Item(name="CAKEPOP", type=6, price=2.5),
    "CROISSANT": Item(name="CROISSANT", type=7, price=3.25),
    "MUFFIN": Item(name="MUFFIN", type=8, price=3),
    "CROISSANT_CHOCOLATE": Item(name="CROISSANT_CHOCOLATE", type=9, price=3.5),
}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/v1/api/item-types")
async def get_item_types() -> list[Item]:
    return [x for x in items.values()]


@app.get("/v1/api/items-by-types/{item_types}")
async def get_items_by_types(item_types: str) -> list[Item]:
    results = []
    inputs = item_types.split(",")
    for i in inputs:
        if items.get(i):
            results.append(items.get(i))
    return results
