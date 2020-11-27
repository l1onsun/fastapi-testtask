from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from database.crud import Session

router = APIRouter()

@router.get("/{user_id}")
async def managers(user_id: str):
    async with AsyncSession(engine) as session:
        return {"hello": "world"} # ToDo