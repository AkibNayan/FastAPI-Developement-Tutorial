from fastapi import FastAPI 
from pydantic import BaseModel, EmailStr
from typing import Union

app = FastAPI()

#Pydantic models  
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    fullname: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    fullname: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    fullname: str | None = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! .. not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# Reduce duplication
class UserBase(BaseModel):
    username: str
    email: EmailStr
    fullname: str | None = None

class UserIn1(UserBase):
    password: str

class UserOut1(UserBase):
    pass

class UserInDB1(UserBase):
    hashed_password: str
    
def fake_password_hasher1(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user1(user_in: UserIn1):
    hashed_password = fake_password_hasher1(user_in.password)
    user_in_db = UserInDB1(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! .. not really")
    return user_in_db

@app.post("/user1/", response_model=UserOut1)
async def create_user(user_in: UserIn1):
    user_saved = fake_save_user1(user_in)
    return user_saved

# Union or anyOf
class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive low rider", "type": "car"},
    "item2": {"description": "Music is my aeroplane", "type": "plane", "size": 5}
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

# List of models
class Item(BaseModel):
    name: str
    description: str
items1 = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]
@app.get("/items/", response_model=list[Item])
async def read_items():
    return items1