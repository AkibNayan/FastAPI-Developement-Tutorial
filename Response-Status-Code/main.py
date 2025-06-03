from fastapi import FastAPI, status, Form
from typing import Annotated
from pydantic import BaseModel 


app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}

# Form Data
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

# Form Models[Pydantic Models for Forms]
class FormData(BaseModel):
    model_config = {"extra": "forbid"}
    username: str
    password: str
    

@app.post("/login-model/")
async def login_model(form_data: Annotated[FormData, Form()]):
    return form_data