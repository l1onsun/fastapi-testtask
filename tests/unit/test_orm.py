import pytest

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import orm
from database.root import DatabaseManager
from tests.scripts.seed_database import drop_and_create, seed_database


@pytest.fixture()
async def db_manager() -> DatabaseManager:
    db_manager = DatabaseManager()
    await drop_and_create(db_manager)
    yield db_manager
    await seed_database(db_manager)

@pytest.mark.asyncio
async def test_single_user(db_manager: DatabaseManager):
    async with db_manager.session(write=True) as session:
        session: AsyncSession

        session.add(orm.User(name="Foo", role=orm.GlobalRoleEnum.employee))
        await session.commit()

        stmt = sa.select(orm.User).where(orm.User.name == "Foo")

        result = await session.execute(stmt)

        user = result.scalar_one()
        assert type(user) is orm.User
        assert user.name == "Foo"
        assert user.company is None


@pytest.mark.asyncio
async def test_two(db_manager: DatabaseManager):
    async with db_manager.session(write=True) as session:
        session: AsyncSession

        new_user = orm.User(name="User Foo", role=orm.GlobalRoleEnum.employee)
        new_project = orm.Project(name="Project Bar")
        new_membership = orm.Membership(
            user=new_user, project=new_project, role=orm.ProjectRoleEnum.manager
        )
        session.add_all([new_user, new_project, new_membership])
        await session.commit()

        stmt = sa.select(orm.User).where(
            orm.User.name == "User Foo"
        ).options(
            selectinload(orm.User.memberships)
                .selectinload(orm.Membership.project)
        )

        result = await session.execute(stmt)
        user = result.scalar_one()

        assert type(user) is orm.User

        assert len(user.memberships) == 1
        assert type(user.memberships[0]) is orm.Membership
        membership: orm.Membership = user.memberships[0]
        assert membership.role == orm.ProjectRoleEnum.manager
        assert membership.project.name == "Project Bar"

#
# @pytest.mark.asyncio
# async def test_three(session_manager):
#     async with session_manager(write=True) as session:
#         c = orm.User(name="foo", role=orm.GlobalRoleEnum.employee)
#         session.add(c)
#         await session.commit()
#         assert len((await session.execute(sa.select(orm.User))).scalars().all()) > 3
