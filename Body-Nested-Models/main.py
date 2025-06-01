from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

#Pydantic Model
#List Fields
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    #For list type
    tags: list[str] = []
    #For set type[With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.]
    tags_set: set[str] = set() 

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

# Nested Models
class Image(BaseModel):
    url: str
    name: str

class Item1(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None

@app.put("/items1/{item_id}")
async def update_item(item_id: int, item: Item1):
    results = {"item_id": item_id, "item": item}
    return results

# Special types and validation
from pydantic import HttpUrl

class Image2(BaseModel):
    url: HttpUrl
    name: str
class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image2 | None = None
@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item2):
    results = {"item_id": item_id, "item": item}
    return results

# Attributes with lists of submodels[You can also use Pydantic models as subtypes of list, set]
class Item3(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image2] | None = None
@app.put("/items3/{item_id}")
async def update_item(item_id: int, item: Item3):
    results = {"item_id": item_id, "item": item}
    return results

# Deeply nested models[You can nest Pydantic models as deeply as you want]
class Item4(BaseModel):
    name: str 
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image2 | None = None
class Offer(BaseModel):
    name: str 
    description: str | None = None
    price: float
    item: list[Item4]
@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

# Bodies of pure lists
@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image2]):
    img = []
    for image in images:
        img.append(image.url)
    return img