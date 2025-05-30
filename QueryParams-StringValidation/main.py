from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

@app.get("/items/")
async def read_items(q: str | None = None):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q is not None:
        result.update({"q": q})
    return result

# Additional Validation
"""We are going to enforce that even though q is optional, whenever it is provided, its length doesn't exceed 50 characters."""

@app.get("/items-val/")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result

# Query parameter list / multiple values
@app.get("/items-list/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {}
    if q:
        query_items = {"q": q}
    return query_items

# Query parameter list / multiple values with defaults
@app.get("/items-list-default/")
async def read_items(q: Annotated[list[str] | None, Query()] = ["Hasnain", "Shahid"]):
    query_items = {}
    if q:
        query_items.update({"q": q})
    return query_items

@app.get("/items-list-default1")
async def read_items(q: Annotated[list | None, Query()] = []):
    query_items = {}
    if q:
        query_items.update({"q": q})
    return query_items

# You can add a title, des, alias
@app.get("/items-list1")
async def read_items(q: Annotated[str | None, Query(title="Query string", description="Hello description", alias="item-query", min_length=3)] = None):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result

@app.get("/items-list2")
async def read_items(q: Annotated[str | None, Query(title="Query string", description="Hello description", alias="item-query", min_length=3, max_length=50, deprecated=True)] = None):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result
# Exclude parameters from OpenAPI
@app.get("/items-list3")
async def read_items(hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not Found"}
    
# Custom Validation
from pydantic import AfterValidator 
import random

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2"
}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid ID format")
    return id

@app.get("/items-list4/")
async def read_items(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}