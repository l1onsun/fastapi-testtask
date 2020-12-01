from database import orm
from database.models import Manager, DetailManager

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import logging; import config.log
import time
from typing import Optional, List, Dict, Set
from uuid import UUID

logger = logging.getLogger(__name__)


def auto_log(func):
    def new_func(*args, **kwargs):
        start_time = time.time()
        logger.info("Start operation: {}".format(func.__name__))
        result = func(*args, **kwargs)
        time_took = time.time() - start_time
        logger.info("Complete operation: {}. Time took: {} seconds".format(func.__name__, time_took))
        return result

    return new_func


@auto_log
async def get_user(user_id: UUID, session: AsyncSession) -> Optional[orm.User]:
    result = await session.execute(
        sa.select(orm.User).where(orm.User.id == user_id)
    )
    return result.scalar_one_or_none()


@auto_log
async def get_owner_managers(owner: orm.User, session: AsyncSession) -> Set[Manager]:
    result = await session.execute(
        sa.select(orm.User.id, orm.User.name).where(
            sa.and_(
                orm.User.company_id == owner.company_id,
                orm.User.id != owner.id)
        )
    )
    return {Manager(id=row[0], name=row[1]) for row in result}  # todo is it optimal ?


@auto_log
async def get_user_memberships(user_id: UUID, session: AsyncSession) -> List[orm.Membership]:
    result = await session.execute(
        sa.select(orm.Membership).where(
            orm.Membership.user_id == user_id
        ).options(
            selectinload(orm.Membership.project)
        )
    )
    return result.scalars().all()


@auto_log
async def get_user_with_memberships(user_id: UUID, session: AsyncSession) -> orm.User:
    result = await session.execute(
        sa.select(orm.User).where(
            orm.User.id == user_id
        ).options(
            selectinload(orm.User.memberships)
            # .selectinload(orm.Membership.project) # load project names?
        )
    )
    return result.scalar_one_or_none()


@auto_log
async def get_project_managers(project_id: UUID, session: AsyncSession) -> Set[Manager]:
    result = await session.execute(
        sa.select(orm.Membership).where(
            sa.and_(
                orm.Membership.project_id == project_id,
                orm.Membership.role == orm.ProjectRoleEnum.manager
            )
        ).options(
            selectinload(orm.Membership.user)
        )
    )
    memberships: List[orm.Membership] = result.scalars().all()
    return {Manager.from_orm(m.user) for m in memberships}


@auto_log
async def find_managers(user_id: UUID, session: AsyncSession) -> Optional[Set[Manager]]:
    user = await get_user_with_memberships(user_id, session=session)
    found_managers: Set[Manager] = set()

    # no user with such uuid
    if not user:
        return None

    # if user is owner of company: add all company managers to found_managers
    if user.role == orm.GlobalRoleEnum.owner:
        managers = await get_owner_managers(user, session=session)
        found_managers |= managers
    else:
        # if user is employee he will found himself
        found_managers.add(Manager.from_orm(user))

    # check memberships in projects
    for membership in user.memberships:
        membership: orm.Membership
        # if user is admin of project: add all project members to found_managers
        if membership.role is orm.ProjectRoleEnum.admin:
            managers = await get_project_managers(membership.project_id, session=session)
            found_managers |= managers


    return found_managers

@auto_log
async def all_managers(session: AsyncSession) -> List[DetailManager]:
    result = await session.execute(
        sa.select(orm.User).options(
            selectinload(orm.User.company),
            selectinload(orm.User.memberships).selectinload(orm.Membership.project)
        )
    )
    return [DetailManager.from_user(user) for user in result.scalars()]
