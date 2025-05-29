# Query parameter type conversion
from fastapi import FastAPI 

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item

# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item 

# Required Query Parameters
@app.get("/item/{item_id}")
async def read_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

# And of course, you can define some parameters as required, some as having a default value, and some entirely optional:
@app.get("/item-part/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: int | None = None):
    item = {
        "item_id": item_id,
        "needy": needy,
        "skip": skip,
        "limit": limit
    }
    return item