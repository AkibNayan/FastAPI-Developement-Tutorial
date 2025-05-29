from fastapi import FastAPI 

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

from enum import Enum

class ModelName(str, Enum):
    alexnet1 = "alexnet"
    resnet1 = "resnet"
    lenet1 = "lenet"
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet1:
        return {"model name": {model_name}, "message": "Deep Learning FTW!"}
    if model_name.value == 'lenet1':
        return {"model name": {model_name.value}, "message": "LeCNN all the images"}
    else:
        return {"model name": {model_name}, "message": "Have some residuals"}