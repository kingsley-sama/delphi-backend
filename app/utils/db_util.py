from typing import Annotated
from database import get_db
from sqlalchemy.orm import Session
from models import User
from fastapi import  Depends
async def find_user_single(username:str, db: Annotated[Session, Depends(get_db)]):
    return(db.query(User).filter(User.username == username).first())
