# Query Parameters with a Pydantic Model

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal

app = FastAPI()

#Pydantic Model
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100) # controls how many results to return default=100
    offset: int = Field(0, ge=0)  # offset is used to skip result default=0
    order_by: Literal['created_at', 'udpated_at'] = 'created_at'
    tags: list[str] = []
    
@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


# Forbid Extra Query Parameters

#pydantic Models
class QueryParams(BaseModel):
    
    model_config = {"extra": "forbid"}
    
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal['created_at', 'updated_at'] = 'created_at'
    tags: list[str] = []
    
@app.get('/items1/')
async def read_items(filter_params: Annotated[QueryParams, Query()]):
    return filter_params
    