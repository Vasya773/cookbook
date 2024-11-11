import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from ..main import app
from ..database import DATABASE_URL, Base


@pytest.fixture(scope="session")
async def database_engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


@pytest.fixture(scope="function")
async def db_session(database_engine):
    async with database_engine.connect() as connection:
        await connection.begin()
        Session = sessionmaker(bind=connection, class_=AsyncSession)
        async with Session() as session:
            yield session
            await session.rollback()


@pytest.fixture()
def client(db_session):
    app.state.database_session = db_session
    with TestClient(app) as client:
        yield client
