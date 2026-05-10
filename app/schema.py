from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
class Tags(Enum):
    users = "users"

class UserBase(BaseModel):
    username : str = Field(min_length=3, max_length=30)
    email : EmailStr

class UserCreate(UserBase):
    password: str

class ReturnUser(UserBase):
    id:UUID
    created_at:datetime

class EmailSchema(BaseModel):
    from_email: EmailStr
    to: EmailStr
    subject: str
    html: str
    
    class Config:
        populate_by_name = True 