from fastapi import FastAPI 
from pydantic import BaseModel 

app = FastAPI()
# Data Model as class
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
"""@app.post("/items")
async def create_item(item: Item):
    return item"""
# Use the model as a request body
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Request body + path parameters
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

# Request body + path + query parameters
@app.put("/item-part/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    # This unpacks the dictionary returned by item.model_dump() and merges its key-value pairs into the returned dictionary.
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

"""If the parameter is also declared in the path, it will be used as a path parameter.
If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body."""