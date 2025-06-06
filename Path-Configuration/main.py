from fastapi import FastAPI, status
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

# Tags
@app.post("/items1/", tags=["items"])
async def create_item1(item: Item):
    return item

@app.get("/items1/", tags=["items"])
async def read_items():
    return [{"name": "Item 1", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "JohnDoe"}]

# Tags with Enums
class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/items2/", tags=[Tags.items])
async def get_items():
    return ["Portal Gun", "Plumbus"]

@app.get("/users1/", tags=[Tags.users])
async def get_users():
    return ["Rick", "Morty"]

# Summary and description
@app.post("/items3/", response_model=Item, summary="Create an item", description="Create an item with all the information, like its name, description, price, tax and a set of unique tags")
async def create_item(item: Item):
    return item

# Description from docstring
@app.post("/items4/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# Response description
@app.post("/items5/", response_model=Item, summary="Create an item", response_description="Created Item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

#Deprecate a path operation
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]

# JSON Compatible Encoder
fake_db = {}

class Item1(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

@app.put("/items6/{id}")
def update_item(id: str, item: Item1):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    return fake_db
