import pytest
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = orm.declarative_base()


class Country(Base):
    __tablename__ = "country"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(
        "postgresql://postgres:postres@127.0.0.1:5432/postgres"
    )
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture()
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(engine, create_tabels):
    async with AsyncSession(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_one(session):
    c = Country(name="foo")
    session.add(c)
    await session.commit()
    assert len((await session.execute(sa.select(Country))).scalars().all()) == 1

@pytest.mark.asyncio
async def test_two(session):
    c = Country(name="foo")
    session.add(c)
    await session.commit()
    assert len((await session.execute(sa.select(Country))).scalars().all()) == 1