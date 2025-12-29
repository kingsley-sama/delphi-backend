from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.user_model import User, UserCreate, UserResponse, UserUpdate
from services.user_service import create_user_service, get_user_by_id, update_user_service
from utils.db import get_db
from utils.auth import get_current_active_user, require_role

user_router = APIRouter(prefix='/users', tags=['Users'])

@user_router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user (public registration)"""
    data = await create_user_service(user_data, db)
    return UserResponse(
        id=data.id,
        user_name=data.user_name,
        email=data.email,
        age=data.age,
        role=data.role,
        grade_level=data.grade_level,
        is_active=data.is_active,
        created_at=data.created_at
    )

@user_router.get('/me', response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile"""
    return UserResponse(
        id=current_user.id,
        user_name=current_user.user_name,
        email=current_user.email,
        age=current_user.age,
        role=current_user.role,
        grade_level=current_user.grade_level,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

@user_router.get('/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Get user by ID (admin/teacher only)"""
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(
        id=user.id,
        user_name=user.user_name,
        email=user.email,
        age=user.age,
        role=user.role,
        grade_level=user.grade_level,
        is_active=user.is_active,
        created_at=user.created_at
    )

@user_router.put('/me', response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update current user profile"""
    updated_user = await update_user_service(current_user.id, user_update, db)
    return UserResponse(
        id=updated_user.id,
        user_name=updated_user.user_name,
        email=updated_user.email,
        age=updated_user.age,
        role=updated_user.role,
        grade_level=updated_user.grade_level,
        is_active=updated_user.is_active,
        created_at=updated_user.created_at
    )

@user_router.get('/', response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"])),
    skip: int = 0,
    limit: int = 100
):
    """List all users (admin/teacher only)"""
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return [
        UserResponse(
            id=user.id,
            user_name=user.user_name,
            email=user.email,
            age=user.age,
            role=user.role,
            grade_level=user.grade_level,
            is_active=user.is_active,
            created_at=user.created_at
        )
        for user in users
    ]