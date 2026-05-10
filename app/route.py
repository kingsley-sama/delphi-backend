from schema import Tags
from fastapi import APIRouter, Depends
from database import get_db
from schema import UserCreate, ReturnUser, EmailSchema
from sqlalchemy.orm import Session
from models import User
from typing import Annotated
from typing import Annotated
from utils.require_role import require_role
from security import hash_password
from auth import authenticate_user
from mailing.email_template import verification_email_template
from security import create_access_token
from mailing.email_util import send_mail
from datetime import datetime, timedelta, timezone

  

auth_route = APIRouter(prefix="/auth", tags=[Tags.users])

@auth_route.post("/register",  response_description="user created successfully", response_model=ReturnUser)
def register_user(user: UserCreate, db:Annotated[Session, Depends(get_db)]):
    pwd =  hash_password(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        password_hash = pwd
        )
    token_data = {
          "username": user.username,
          "email": user.email,
          "expires": (datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat()
    }
    token = create_access_token(token_data)
    url = f'http://0.0.0.0:8000/verify-email/{token}'
    html = verification_email_template(token_data["username"], url)
    email_schema  = EmailSchema(
        from_email="kingsley@delphieduhub.com",
        to=token_data["email"],
        subject="verification email",
        html=html,
    )
    send_mail(email_schema)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user



@auth_route.post("/login", response_description="user fetched successfully")
async def login_user(email: str, password: str, db: Annotated[Session, Depends(get_db)]):
    user = await authenticate_user(email, password, db)
    return user
    
          
@auth_route.post("/logout", response_description="user fetched successfully")
def logout_user(user: Annotated[User, Depends(require_role("user"))]):
        return {
        "status":200,
        "message": "logout user",
        "user": f'your account: {user.username} has been logged out successfully'
    }

@auth_route.post("/refresh", response_description="user fetched successfully")
def refresh_token(user: Annotated[User, Depends(require_role("user"))]):
        return {
        "status":200,
        "message": "post user route",
        "user": user.username
    }


@auth_route.get("/me")
async def get_current_user(user: Annotated[User, Depends(require_role("user"))]):
      pass

@auth_route.get("/verify-email/{token}")
def verify_email(token: str):
      pass