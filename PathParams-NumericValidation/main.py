from fastapi import FastAPI, Query, Path
from typing import Annotated 


app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get")], q: Annotated[str | None, Query(alias="item-query")] = None):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result

@app.get("/items1/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result

# Order the parameters as you need, tricks, Pass *, as the first parameter of the function.
@app.get("/items2/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result

# Better with Annotated
@app.get("/items3/{item_id}")
async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get")], q: str):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result
# Number validations: greater than or equal and less than or equal
@app.get("/items4/{item_id}")
async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get", ge=10, le=100)], q: str):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result

# Number validations: floats, greater than and less than
@app.get("/items5/{item_id}")
async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get", ge=10, le=100)], q: str, size: Annotated[float, Query(ge=0, le=10.5)]):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    if size:
        result.update({"size": size})
    return result
