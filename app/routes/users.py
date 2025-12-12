from fastapi import APIRouter, Depends
from services.user_service import create_user_service
from models.user_model import UserCreate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
user_router = APIRouter(prefix='/user')
from utils.db import get_db

@user_router.post(path='/', response_model=UserResponse )
async def new_user(user_data:UserCreate, db:AsyncSession = Depends(get_db)):
    data = await create_user_service(user_data, db)
    return UserResponse(
        user_name=data.user_name,
        age=data.age,
        role=data.role
    )