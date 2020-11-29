from database import orm

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import time
from typing import Optional, List, Dict
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
async def find_managers(user_id: UUID, session: AsyncSession) -> Optional[List[Dict]]:
    print("in find_manager")
    user = await get_user(user_id, session=session)
    print("after get_user")
    if not user:
        return None
    if user.role == orm.GlobalRoleEnum.owner:
        owner = user
        print("in role==owner")
        result = await session.execute(
            sa.select(orm.User.id, orm.User.name).where(
                sa.and_(
                    orm.User.company_id == owner.company_id,
                    orm.User.id != owner.id)
            )
        )
        return [dict(u) for u in result.all()]
    else:
        memberships: orm.Membership = user.memberships
        print(type(memberships))
        print(memberships)
        return [{"name": "Abra"}, {"name": "Cadabra"}]  # todo
