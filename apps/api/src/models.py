# from sqlmodel import SQLModel, Field


# class SongBase(SQLModel):
#     name: str
#     artist: str


# class Song(SongBase, table=True):
#     id: int = Field(default=None, nullable=False, primary_key=True)


# class SongCreate(SongBase):
#     pass


# SongBase is the base model that the others inherit from. It has two properties, name and artist, both of which are strings. This is a data-only model since it lacks table=True, which means that it's only used as a pydantic model.
# Song, meanwhile, adds an id property to the base model. It's a table model, so it's a pydantic and SQLAlchemy model. It represents a database table.
# SongCreate is a data-only, pydantic model that will be used to create new song instances.

from sqlmodel import SQLModel, Field


class BabyBase(SQLModel):
    # id
    # user_id
    given_name: str
    family_name: str
    # dob
    # created_at
    # updated_at


class Baby(BabyBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class BabyCreate(BabyBase):
    pass