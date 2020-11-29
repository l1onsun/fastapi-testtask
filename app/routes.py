from fastapi import APIRouter
from uuid import UUID

from database.crud import find_managers
from .db_manager import db_manager


router = APIRouter()

@router.get("/managers/{user_id}")
async def managers(user_id: UUID):
    async with db_manager.session() as session:
        print("before find_manager")
        return await find_managers(user_id, session=session)