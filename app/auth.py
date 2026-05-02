from security import verify_password, create_access_token
from models import User
from sqlalchemy.orm import Session
from database import get_db
from typing import Annotated
from fastapi import HTTPException, status, Depends 
from security import decode_access_token

def authenticate_user(email:str, password:str, db: Session):
    user = db.query(User).filter(User.email ==  email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def login_user(email:str, password:str, db:Session):
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
    

async def get_current_user(token:Annotated[str, Depends()], db: Annotated[Session, Depends(get_db)]):
    try:
        payload = decode_access_token(token)
        email =  payload.get("sub")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user