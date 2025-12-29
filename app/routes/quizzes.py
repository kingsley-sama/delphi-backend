from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from models.quiz_model import (
    QuizCreate, QuizUpdate, QuizResponse,
    QuizQuestionCreate, QuizQuestionUpdate, QuizQuestionResponse,
    QuizAttemptCreate, QuizAttemptResponse
)
from models.user_model import User
from services.quiz_service import (
    create_quiz_service, get_quiz_by_id, update_quiz_service,
    delete_quiz_service, list_course_quizzes,
    create_question_service, get_question_by_id, update_question_service,
    get_quiz_questions, submit_quiz_attempt, get_user_quiz_attempts,
    get_quiz_attempt_by_id
)
from utils.db import get_db
from utils.auth import get_current_active_user, require_role

quiz_router = APIRouter(prefix='/quizzes', tags=['Quizzes'])

# Quiz Endpoints
@quiz_router.post('/', response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    quiz_data: QuizCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Create a new quiz (admin/teacher only)"""
    quiz = await create_quiz_service(quiz_data, current_user.id, db)
    return QuizResponse(**quiz.model_dump())

@quiz_router.get('/{quiz_id}', response_model=QuizResponse)
async def get_quiz(
    quiz_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get quiz by ID"""
    quiz = await get_quiz_by_id(quiz_id, db)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return QuizResponse(**quiz.model_dump())

@quiz_router.put('/{quiz_id}', response_model=QuizResponse)
async def update_quiz(
    quiz_id: int,
    quiz_update: QuizUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Update quiz (admin/teacher only)"""
    quiz = await update_quiz_service(quiz_id, quiz_update, db)
    return QuizResponse(**quiz.model_dump())

@quiz_router.delete('/{quiz_id}')
async def delete_quiz(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Delete quiz (admin/teacher only)"""
    return await delete_quiz_service(quiz_id, db)

@quiz_router.get('/course/{course_id}', response_model=list[QuizResponse])
async def list_quizzes_for_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all quizzes for a course"""
    quizzes = await list_course_quizzes(course_id, db)
    return [QuizResponse(**quiz.model_dump()) for quiz in quizzes]

# Question Endpoints
@quiz_router.post('/{quiz_id}/questions', response_model=QuizQuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    quiz_id: int,
    question_data: QuizQuestionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Create a new question for a quiz (admin/teacher only)"""
    if question_data.quiz_id != quiz_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz ID mismatch"
        )
    question = await create_question_service(question_data, db)
    return QuizQuestionResponse(**question.model_dump())

@quiz_router.get('/{quiz_id}/questions', response_model=list[QuizQuestionResponse])
async def list_quiz_questions(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    include_answers: bool = Query(False)
):
    """Get all questions for a quiz"""
    # Only allow teachers/admins to see answers
    if include_answers and current_user.role not in ["admin", "teacher"]:
        include_answers = False
    
    questions = await get_quiz_questions(quiz_id, db, include_answers)
    return [QuizQuestionResponse(**question.model_dump()) for question in questions]

@quiz_router.get('/questions/{question_id}', response_model=QuizQuestionResponse)
async def get_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Get question by ID (admin/teacher only)"""
    question = await get_question_by_id(question_id, db)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return QuizQuestionResponse(**question.model_dump())

@quiz_router.put('/questions/{question_id}', response_model=QuizQuestionResponse)
async def update_question(
    question_id: int,
    question_update: QuizQuestionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Update question (admin/teacher only)"""
    question = await update_question_service(question_id, question_update, db)
    return QuizQuestionResponse(**question.model_dump())

# Quiz Attempt Endpoints
@quiz_router.post('/{quiz_id}/attempt', response_model=QuizAttemptResponse)
async def submit_quiz(
    quiz_id: int,
    attempt_data: QuizAttemptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Submit a quiz attempt"""
    if attempt_data.quiz_id != quiz_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz ID mismatch"
        )
    attempt = await submit_quiz_attempt(current_user.id, attempt_data, db)
    return QuizAttemptResponse(**attempt.model_dump())

@quiz_router.get('/{quiz_id}/attempts', response_model=list[QuizAttemptResponse])
async def get_my_quiz_attempts(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's attempts for a quiz"""
    attempts = await get_user_quiz_attempts(current_user.id, quiz_id, db)
    return [QuizAttemptResponse(**attempt.model_dump()) for attempt in attempts]

@quiz_router.get('/attempts/{attempt_id}', response_model=QuizAttemptResponse)
async def get_attempt(
    attempt_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get quiz attempt by ID"""
    attempt = await get_quiz_attempt_by_id(attempt_id, db)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found"
        )
    
    # Users can only view their own attempts unless admin/teacher
    if attempt.user_id != current_user.id and current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this attempt"
        )
    
    return QuizAttemptResponse(**attempt.model_dump())
