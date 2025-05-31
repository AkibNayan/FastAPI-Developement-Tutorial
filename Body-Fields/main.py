from fastapi import FastAPI, Body
from typing import Annotated
from pydantic import BaseModel, Field


app = FastAPI()

#Pydantic Model 
class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, title="This is a description of Item", max_length=300),
    price: float = Field(gt=0, description="The price must be greater than zero"),
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    result = {
        "item_id": item_id,
        "item": item
    }
    return result
