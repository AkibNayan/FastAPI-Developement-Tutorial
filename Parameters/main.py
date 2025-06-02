# Cookie and Header Parameters
from fastapi import FastAPI, Cookie, Header
from typing import Annotated
from pydantic import BaseModel 

app = FastAPI()

@app.get("/items-cookie/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

@app.get("/items-header/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

@app.get("/items-header1/")
async def read_items(strange_header: Annotated[str | None, Header(convert_underscores=False)] = None):
    return {"strange_header": strange_header}


@app.get("/items-header2/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}


# Cookie and Header Parameter Pydantic Models
class Cookies(BaseModel):
    model_config = {"extra": "forbid"}
    
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies

# Header Parameters with a Pydantic Model
class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = None

@app.get("/items1/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers