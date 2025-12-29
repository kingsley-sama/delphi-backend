from sqlmodel import Field, SQLModel, Column, Relationship
from datetime import datetime
from pydantic import BaseModel, EmailStr
import sqlalchemy as sa
from enum import Enum
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.course_model import CourseEnrollment
    from models.quiz_model import QuizAttempt

class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    parent = "parent"
    learner = "learner"

class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    age: int
    role: UserRole = UserRole.learner
    grade_level: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    grade_level: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    user_name: str
    email: str
    age: int
    role: UserRole
    grade_level: Optional[int] = None
    is_active: bool
    created_at: datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    password: str
    age: int
    role: UserRole = Field(
        default=UserRole.learner,
        sa_column=Column(sa.Enum(UserRole, name="user_role_enum"))
    )
    grade_level: int | None = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)