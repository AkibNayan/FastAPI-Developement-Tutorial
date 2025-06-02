from fastapi import FastAPI, Response
from pydantic import BaseModel, EmailStr
from typing import Any
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=32.2),
        Item(name="Plumbus", price=43.2)
    ]
    
# response_model Parameter
@app.post("/items1/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item

@app.get("/items1/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 43.3},
        {"name": "Plumbus", "price": 23.3}
    ]
# Return the same input data
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    fullname: str | None = None
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user

# Add an output model
class UserOut(BaseModel):
    username: str
    email: EmailStr
    fullname: str | None = None
@app.post("/user1/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

# Return Type and Data Filtering
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
class UserIn1(BaseUser):
    password: str
@app.post("/user2/")
async def create_user(user: UserIn) -> BaseModel:
    return user

# Return a Response Directly
@app.get("/portal/")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimentional portal"})

# Annotate a response subclass
@app.get("/teleport/")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Response Model encoding parameters
items = {
    "foo": {"name": "Foo", "price": 30.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []} 
}
@app.get("/items/{item_id}", response_model= Item, response_model_exclude_unset=True)
async def read_items(item_id: str):
    return items[item_id]

# response_model_include and response_model_exclude
@app.get("/items/{item_id}/name", response_model=Item, response_model_include={"name", "description"})
async def read_items(item_id: str):
    return items[item_id]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_items(item_id: str):
    return items[item_id]

# Using lists instead of sets¶
@app.get("/items/{item_id}/name1", response_model=Item, response_model_include=["name", "description"])
async def read_items(item_id: str):
    return items[item_id]

@app.get("/items/{item_id}/public1", response_model=Item, response_model_exclude=["tax"])
async def read_items(item_id: str):
    return items[item_id]
