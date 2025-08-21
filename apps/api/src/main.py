# # from typing import Union
# # from fastapi import FastAPI
# # from pydantic import BaseModel


# from typing import Annotated, Union

# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select
# from pydantic import BaseModel

# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}




# class HeroBase(SQLModel):
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)


# class Hero(HeroBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     secret_name: str


# class HeroPublic(HeroBase):
#     id: int


# class HeroCreate(HeroBase):
#     secret_name: str


# class HeroUpdate(HeroBase):
#     name: str | None = None
#     age: int | None = None
#     secret_name: str | None = None


# # sqlite_file_name = "database.db"
# # sqlite_url = f"sqlite:///{sqlite_file_name}"
# postgresql_file_name = "database.db"
# postgresql_url = f"postgresql:///{postgresql_file_name}"
# # https://<project_ref>.supabase.co/rest/v1/

# # connect_args = {"check_same_thread": False}
# # engine = create_engine(sqlite_url, connect_args=connect_args)
# connect_args = {"check_same_thread": False}
# engine = create_engine(postgresql_url, connect_args=connect_args)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# SessionDep = Annotated[Session, Depends(get_session)]
# app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# @app.post("/heroes/", response_model=HeroPublic)
# def create_hero(hero: HeroCreate, session: SessionDep):
#     db_hero = Hero.model_validate(hero)
#     session.add(db_hero)
#     session.commit()
#     session.refresh(db_hero)
#     return db_hero


# @app.get("/heroes/", response_model=list[HeroPublic])
# def read_heroes(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ):
#     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#     return heroes


# @app.get("/heroes/{hero_id}", response_model=HeroPublic)
# def read_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return hero


# @app.patch("/heroes/{hero_id}", response_model=HeroPublic)
# def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
#     hero_db = session.get(Hero, hero_id)
#     if not hero_db:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     hero_data = hero.model_dump(exclude_unset=True)
#     hero_db.sqlmodel_update(hero_data)
#     session.add(hero_db)
#     session.commit()
#     session.refresh(hero_db)
#     return hero_db


# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}


from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .db import get_session, init_db
from .models import Baby, BabyCreate

app = FastAPI()

# @app.on_event("startup")
# async def on_startup():
#     await init_db()

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

# @app.get("/songs", response_model=list[Song])
# async def get_songs(session: AsyncSession = Depends(get_session)):
#     result = await session.execute(select(Song))
#     songs = result.scalars().all()
#     return [Song(name=song.name, artist=song.artist, id=song.id) for song in songs]

@app.get("/babies", response_model=list[Baby])
async def get_babies(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Baby))
    babies = result.scalars().all()
    return [Baby(given_name=baby.given_name, family_name=baby.family_name) for baby in babies]

# @app.post("/songs")
# async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
#     song = Song(name=song.name, artist=song.artist)
#     session.add(song)
#     await session.commit()
#     await session.refresh(song)
#     return song

@app.post("/babies")
async def add_baby(baby: BabyCreate, session: AsyncSession = Depends(get_session)):
    baby = Baby(given_name=baby.given_name, family_name=baby.family_name)
    session.add(baby)
    await session.commit()
    await session.refresh(baby)
    return baby