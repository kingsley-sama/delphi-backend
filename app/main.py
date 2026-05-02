from fastapi import FastAPI, Depends, HTTPException, status
from route import user_route
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from schema import UserBase
from database import get_db
from typing import Annotated
from utils import find_user_single
from schema import ReturnUser
from sqlalchemy.orm import Session

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(user_route)

@app.get("/")
def get():
    return {"body": "welcome to delphi ai"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)