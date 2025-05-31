from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

# Pydantic Model
class Item(BaseModel):
    #Query Parameter
    name: str
    description: str = None
    price: float
    tax: float = None

@app.put("/items/{item_id}")
async def update_item(item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)], q: str | None = None, item: Item | None = None):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    if item:
        result.update({"item": item})
    return result

# You can also declare multiple body parameters  
class User(BaseModel):
    username: str
    fullname: str | None = None 
@app.put("/items1/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    result = {
        "item_id": item_id,
        "item": item,
        "user": user
    }
    return result 

# Singular values in body
@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: Annotated[int, Body()]):
    result = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }
    return result