from fastapi import FastAPI
from database import db_engine
from route import user_route
from typing import Annotated
from models import Base
import models
import uvicorn


app = FastAPI()
Base.metadata.create_all(bind=db_engine)
app.include_router(user_route)

@app.get("/")
def get():
    return {"body": "welcome to delphi ai"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)