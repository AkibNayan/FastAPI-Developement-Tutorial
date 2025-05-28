def get_full_name(first_name:str, last_name:str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

#print(get_full_name("john", "doe"))

def get_name_with_age(name:str, age:int):
    with_name_age = name + " is years old: "+ str(age)
    return with_name_age

#print(get_name_with_age("John doe", 25))

def get_item(item_a:str, item_b:int, item_c:float, item_d:bool, item_e:bytes):
    return item_a, item_b, item_c, item_d, item_e

#print(get_item("John", 25, 3.14, True, b"Hello"))

def process_items(items: list[str, str, str]):
    for item in items:
        print(item)

#print(process_items(["apple", "banana", "cherry"]))

def process_items1(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(f"{item_name} costs {item_price}")
        
#print(process_items1({"apple": 0.5, "banana": 0.3, "cherry": 0.8}))
from typing import Union
def process_items2(items: Union[str, int]):
    return items
#print(process_items2("hello"))

from typing import Optional
def say_hi(name: Optional[str] = None):
    if name is not None:
        return f"Hello {name}"
    else:
        return "Hello World"

#print(say_hi("Akib"))
def say_hi1(name: str = None):
    if name is not None:
        return f"Hello {name}"
    else:
        return "Hello World"

#print(say_hi1())

class Person:
    def __init__(self, name: str=None):
        self.name = name
def get_person_name(one_person: Person):
    return one_person.name
############# 
#Pydantic
from datetime import datetime 
from pydantic import BaseModel 

class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []
    
external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22:00",
    "friends": [1, "2", b"3"]
}

user = User(**external_data)
#print(user)
#print(user.id)

from typing import Annotated
def say_hello(name: Annotated[str, "This is just metadata"]) -> str:
    return f"Hello {name}"
print(say_hello("akib"))
    
