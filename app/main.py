#!/usr/bin/env python3
from fastapi import FastAPI
from routes.users import user_router
from contextlib import asynccontextmanager
from utils.db import init_db




@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)



@app.get('/')
def main():
    return{"message": "hello world"}





if __name__ == "__main__":
    import uvicorn
    from core.config import settings
    uvicorn.run("main:app", port=settings.PORT, reload=True)