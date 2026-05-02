from schema import Tags
from fastapi import APIRouter, Depends
from database import get_db
from schema import UserCreate, ReturnUser
from sqlalchemy.orm import Session
from models import User
from typing import Annotated
from typing import Annotated
from utils.require_role import require_role
from security import hash_password
user_route = APIRouter(prefix="/users", tags=[Tags.users])


@user_route.get("/")
def fetch_all_user():
    return {
        "status":200,
        "message": "get user route"
    }

@user_route.post("/{username}", response_description="user fetched successfully")
def fetch_single_user(username: str):
        return {
        "status":200,
        "message": "post user route",
        "user": username
    }


@user_route.post("/",  response_description="user created successfully", response_model=ReturnUser)
def create_user(user: UserCreate, db:Annotated[Session, Depends(get_db)]):
    pwd =  hash_password(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        password_hash = pwd
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user_route.get("/me")
async def get_current_user(user: Annotated[User, Depends(require_role("user"))]):
      return {"message": f'welcome: {user.username}'}