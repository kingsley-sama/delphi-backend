from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.user_model import User, UserCreate, UserUpdate
from utils.hash_password import hash_password

async def create_user_service(user_data: UserCreate, db: AsyncSession):
    """Create a new user"""
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    result = await db.execute(
        select(User).where(User.user_name == user_data.user_name)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Hash password and create user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        user_name=user_data.user_name,
        email=user_data.email,
        password=hashed_password,
        age=user_data.age,
        role=user_data.role,
        grade_level=user_data.grade_level
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(user_id: int, db: AsyncSession):
    """Get user by ID"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def update_user_service(user_id: int, user_update: UserUpdate, db: AsyncSession):
    """Update user information"""
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields if provided
    if user_update.user_name is not None:
        user.user_name = user_update.user_name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.age is not None:
        user.age = user_update.age
    if user_update.grade_level is not None:
        user.grade_level = user_update.grade_level
    
    await db.commit()
    await db.refresh(user)
    return user