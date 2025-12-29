"""
Routes package - exports all routers
"""
from routes.auth import auth_router
from routes.users import user_router
from routes.courses import course_router
from routes.quizzes import quiz_router
from routes.ai import ai_router

__all__ = [
    "auth_router",
    "user_router",
    "course_router",
    "quiz_router",
    "ai_router",
]
