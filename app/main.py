#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from utils.db import init_db

# Import all routers
from routes.auth import auth_router
from routes.users import user_router
from routes.courses import course_router
from routes.quizzes import quiz_router
from routes.ai import ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Delphi Educational Platform Backend API",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(course_router)
app.include_router(quiz_router)
app.include_router(ai_router)


@app.get('/')
def root():
    return {
        "message": "Welcome to Delphi Educational Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get('/health')
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)