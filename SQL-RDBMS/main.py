from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

#Create Models
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

#Create sqlite Engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Create a DB tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Create a session dependency
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero, session: Annotated[Session, Depends(get_session)]) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# Read Heroes
@app.get("/heroes/")
def read_heroes(session: Annotated[Session, Depends(get_session)], offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# Read One Hero
@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: Annotated[Session, Depends(get_session)]) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# Delete a Hero
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Annotated[Session, Depends(get_session)]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"Ok": True}