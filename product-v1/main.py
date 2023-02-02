from decimal import *
import time
from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging

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

logger = logging.getLogger("uvicorn.error")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logger.info(str(request.url))
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/api1")
def read_root_api1():
    return {"Hello": "From Api1"}


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
