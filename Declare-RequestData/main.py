from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

@app.get("/")
async def root():
    return {"hello": "world"}

# Extra JSON Schema data in Pydantic models[Pydantic v1]
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice item",
                    "price": 35.6,
                    "tax": 3.2
                }
            ]
        }
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
# Extra JSON Schema data in Pydantic models[Pydantic v2]
class Item1(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None 
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "This is nice Item",
                    "price": 32.2,
                    "tax": 0.4,
                    "vat": 0.45
                }
            ]
        }
    }
@app.put("/items1/{item_id}")
async def update_item(item_id: int, item: Item1):
    result = {"item_id": item_id, "item": item}
    return result

class Item2(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["This is nice Item"])
    price: float = Field(examples=[32.2])
    tax: float | None = Field(default=None, examples=[0.4])
    
@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item):
    result = {"item_id": item_id, "item": item}
    return result

# Body with examples
class Item3(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.put("/items3/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[Item3, Body(examples=[{
        "name": "Foo",
        "description": "This is nice Item",
        "price": 32.2,
        "tax": 0.4 
    }])]
):
    result = {"item_id": item_id, "item": item}
    return result

# Body with multiple examples
@app.put("/items4/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[Item3, Body(
        examples=[
            {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
        ]
    )]
):
    result = {"item_id": item_id, "item": item}
    return result

# Using the openapi_examples Parameter
@app.put("/items5/{item_id}")
async def update_item(
    *, 
    item_id: int,
    item: Annotated[Item3, Body(
        openapi_examples = {
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** items works correctly",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                }
            },
            "converted": {
                "summary": "An examples with converted data",
                "description": "FastAPI can convert price 'strings' to actual",
                "value": {
                    "name": "Bar",
                    "price": 53.2
                }
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four"
                }
            }
        }
    )]
):
    result = {"item_id": item_id, "item": item}
    return result