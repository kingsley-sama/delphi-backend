from sqlmodel import Field, SQLModel, Column
from datetime import datetime
from pydantic import BaseModel
import sqlalchemy as sa
from enum import Enum
class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    parent = "parent"
    learner = "learner"

class UserCreate(BaseModel):
    user_name: str
    password: str
    age: int
    role: UserRole = UserRole.learner

class UserResponse(BaseModel):
    user_name: str
    age: int
    role: UserRole = UserRole.learner


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_name:str
    password:str
    age: int
    role: UserRole = Field(
        default=UserRole.learner,
        sa_column=Column(sa.Enum(UserRole, name="user_role_enum"))
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())