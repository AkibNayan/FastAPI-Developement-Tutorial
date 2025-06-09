from fastapi import FastAPI, Depends, Cookie, HTTPException, Header
from typing import Annotated, Any

app = FastAPI()

# Dependency
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# share Annotated dependencies
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/items1/")
async def read_items(commons: CommonsDep):
    return commons


@app.get("/users1/")
async def read_users(commons: CommonsDep):
    return commons

# Classes as dependencies
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items2/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

# Type annotation vs Depends
@app.get("/items3/")
async def read_items(commons: Annotated[Any, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

# shortcut for Depends
@app.get("/items4/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

# Sub-dependencies
def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(q: Annotated[str, Depends(query_extractor)], last_query: Annotated[str | None, Cookie()] = None):
    if not q:
        return last_query
    return q

@app.get("/items5/")
async def read_query(query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]):
    return {"q_or_cookie": query_or_default}

# Dependencies in path operation decorators
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != 'fake_super_secret_token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != 'fake_super_secret_key':
        raise HTTPException(status_code=400, detail='X-Key header invalid')
    return x_key

@app.get("/items6/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


