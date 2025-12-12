from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils.db import get_db
from models.user_model import User
async def create_user_service( user_data, db:AsyncSession):
    new_user = User(
        user_name=user_data.user_name,
        password=user_data.password,
        age=user_data.age
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user