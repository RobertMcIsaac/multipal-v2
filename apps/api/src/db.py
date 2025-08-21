# import os

# from sqlmodel import create_engine, SQLModel, Session


# DATABASE_URL = os.environ.get("DATABASE_URL")

# engine = create_engine(DATABASE_URL, echo=True)


# def init_db():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# Initialized a new SQLAlchemy engine using create_engine from SQLModel. The major differences between SQLModel's create_engine and SQLAlchemy's version is that the SQLModel version adds type annotations (for editor support) and enables the SQLAlchemy "2.0" style of engines and connections. Also, we passed in echo=True so we can see the generated SQL queries in the terminal. This is always nice to enable in development mode for debugging purposes.
# Created a SQLAlchemy session.



import os

from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker

# We used the SQLAlchemy constructs -- i.e., AsyncEngine and AsyncSession -- since SQLModel does not have wrappers for them as of writing.
# We disabled expire on commit behavior by passing in expire_on_commit=False.
# metadata.create_all doesn't execute asynchronously, so we used run_sync to execute it synchronously within the async function.

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session