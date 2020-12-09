from database import orm
from database.models import Manager, DetailManager

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import logging;
import config.log
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
    return {Manager(id=row[0], name=row[1]) for row in result}


@auto_log
async def get_user_admin_memberships(user_id: UUID, project_id=None, session: AsyncSession = ...) \
        -> List[orm.Membership]:
    if project_id is None:
        stmt = sa.select(orm.Membership).where(
            sa.and_(
                orm.Membership.user_id == user_id,
                orm.Membership.role == orm.ProjectRoleEnum.admin
            )
        )
    else:
        stmt = sa.select(orm.Membership).where(
            sa.and_(
                orm.Membership.user_id == user_id,
                orm.Membership.role == orm.ProjectRoleEnum.admin,
                orm.Membership.project_id == project_id
            )
        )
        # ).options(
        #     selectinload(orm.Membership.project)  # todo do i need project?
        # )
    result = await session.execute(stmt)
    return result.scalars().all()


@auto_log
async def get_projects_managers(projects: List[UUID], session: AsyncSession) -> Set[Manager]:
    print("$$$", projects, "$$$")
    result = await session.execute(
        sa.select([orm.Membership], orm.Membership.project_id.in_(projects))
            .options(
            selectinload(orm.Membership.user)
        )
    )
    memberships: List[orm.Membership] = result.scalars().all()
    return {Manager.from_orm(m.user) for m in memberships}


@auto_log
async def find_managers(user_id: UUID, project_id=None, session: AsyncSession = ...) -> Optional[Set[Manager]]:
    user = await get_user(user_id, session=session)
    if not user:
        return None

    admin_memberships = await get_user_admin_memberships(user_id, project_id=project_id, session=session)
    found_managers: Set[Manager] = set()

    # if user is owner of company: add all company managers to found_managers
    if user.role == orm.GlobalRoleEnum.owner:
        managers = await get_owner_managers(user, session=session)
        found_managers |= managers
    else:
        # if user is employee he will found himself
        found_managers.add(Manager.from_orm(user))

    # check memberships in projects
    found_managers |= await get_projects_managers([am.project_id for am in admin_memberships],
                                                  session=session)  # todo: one request

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
