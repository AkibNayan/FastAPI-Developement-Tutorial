from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# HeroBase - the base class
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    
# Hero - the table model
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str

# HeroPublic - the public data model
class HeroPublic(HeroBase):
    id: int

# HeroCreate - the data model to create a hero
class HeroCreate(HeroBase):
    secret_name: str

# HeroUpdate - the data model to update a hero
class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
    
# Create engine
sqlite_file_name = "sql_security.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Create a new session
def get_session():
    with Session(engine) as session:
        yield session

# Dependency
SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Create with HeroCreate and return a HeroPublic
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: Annotated[Session, Depends(get_session)]):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# Read Heroes with HeroPublic
@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(session: Annotated[Session, Depends(get_session)], offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# Read One Hero with HeroPublic
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: Annotated[Session, Depends(get_session)]):
    hero = session.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# Update a Hero with HeroUpdate
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: Annotated[Session, Depends(get_session)]):
    hero_db = session.get(Hero, hero_id)
    if hero_db is None:
        raise HTTPException(status_code=404, detail="Hero Not Found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

# Delete a Hero Again
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Annotated[Session, Depends(get_session)]):
    hero = session.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Hero Not Found")
    session.delete(hero)
    session.commit()
    return {"Ok": True}
    
