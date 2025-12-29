from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Dict, Any
from datetime import datetime
from models.quiz_model import (
    Quiz, QuizCreate, QuizUpdate,
    QuizQuestion, QuizQuestionCreate, QuizQuestionUpdate,
    QuizAttempt, QuizAttemptCreate
)

async def create_quiz_service(quiz_data: QuizCreate, creator_id: int, db: AsyncSession):
    """Create a new quiz"""
    new_quiz = Quiz(
        course_id=quiz_data.course_id,
        lesson_id=quiz_data.lesson_id,
        title=quiz_data.title,
        description=quiz_data.description,
        time_limit_minutes=quiz_data.time_limit_minutes,
        passing_score=quiz_data.passing_score,
        difficulty_level=quiz_data.difficulty_level,
        created_by=creator_id
    )
    db.add(new_quiz)
    await db.commit()
    await db.refresh(new_quiz)
    return new_quiz

async def get_quiz_by_id(quiz_id: int, db: AsyncSession):
    """Get quiz by ID"""
    result = await db.execute(
        select(Quiz).where(Quiz.id == quiz_id)
    )
    return result.scalar_one_or_none()

async def update_quiz_service(quiz_id: int, quiz_update: QuizUpdate, db: AsyncSession):
    """Update quiz information"""
    quiz = await get_quiz_by_id(quiz_id, db)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    update_data = quiz_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(quiz, key, value)
    
    await db.commit()
    await db.refresh(quiz)
    return quiz

async def delete_quiz_service(quiz_id: int, db: AsyncSession):
    """Delete a quiz"""
    quiz = await get_quiz_by_id(quiz_id, db)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    await db.delete(quiz)
    await db.commit()
    return {"message": "Quiz deleted successfully"}

async def list_course_quizzes(course_id: int, db: AsyncSession):
    """Get all quizzes for a course"""
    result = await db.execute(
        select(Quiz).where(Quiz.course_id == course_id)
    )
    return result.scalars().all()

# Question Services
async def create_question_service(question_data: QuizQuestionCreate, db: AsyncSession):
    """Create a new quiz question"""
    # Verify quiz exists
    quiz = await get_quiz_by_id(question_data.quiz_id, db)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    new_question = QuizQuestion(
        quiz_id=question_data.quiz_id,
        question_text=question_data.question_text,
        question_type=question_data.question_type,
        options=question_data.options,
        correct_answer=question_data.correct_answer,
        explanation=question_data.explanation,
        points=question_data.points,
        order_index=question_data.order_index
    )
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return new_question

async def get_question_by_id(question_id: int, db: AsyncSession):
    """Get question by ID"""
    result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.id == question_id)
    )
    return result.scalar_one_or_none()

async def update_question_service(question_id: int, question_update: QuizQuestionUpdate, db: AsyncSession):
    """Update question information"""
    question = await get_question_by_id(question_id, db)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    update_data = question_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(question, key, value)
    
    await db.commit()
    await db.refresh(question)
    return question

async def get_quiz_questions(quiz_id: int, db: AsyncSession, include_answers: bool = False):
    """Get all questions for a quiz"""
    result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id).order_by(QuizQuestion.order_index)
    )
    questions = result.scalars().all()
    
    if not include_answers:
        # Remove correct answers for quiz takers
        for question in questions:
            question.correct_answer = None
    
    return questions

# Quiz Attempt Services
async def submit_quiz_attempt(user_id: int, attempt_data: QuizAttemptCreate, db: AsyncSession):
    """Submit and grade a quiz attempt"""
    # Get quiz
    quiz = await get_quiz_by_id(attempt_data.quiz_id, db)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Get all questions with answers
    questions = await get_quiz_questions(attempt_data.quiz_id, db, include_answers=True)
    
    # Grade the quiz
    score = 0
    total_points = 0
    graded_answers = {}
    
    for question in questions:
        total_points += question.points
        question_id = str(question.id)
        
        if question_id in attempt_data.answers:
            user_answer = attempt_data.answers[question_id]
            is_correct = check_answer(user_answer, question.correct_answer, question.question_type)
            
            graded_answers[question_id] = {
                "user_answer": user_answer,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "points_earned": question.points if is_correct else 0,
                "explanation": question.explanation
            }
            
            if is_correct:
                score += question.points
    
    # Calculate percentage
    percentage = (score / total_points * 100) if total_points > 0 else 0
    passed = percentage >= quiz.passing_score
    
    # Create attempt record
    new_attempt = QuizAttempt(
        quiz_id=attempt_data.quiz_id,
        user_id=user_id,
        score=score,
        total_points=total_points,
        percentage=percentage,
        answers=graded_answers,
        time_taken_minutes=None,  # Can be calculated from frontend
        passed=passed
    )
    
    db.add(new_attempt)
    await db.commit()
    await db.refresh(new_attempt)
    return new_attempt

def check_answer(user_answer: str, correct_answer: str, question_type: str) -> bool:
    """Check if user's answer is correct"""
    if question_type == "multiple_choice" or question_type == "true_false":
        return user_answer.strip().lower() == correct_answer.strip().lower()
    elif question_type == "short_answer":
        # Simple string comparison (can be enhanced with fuzzy matching)
        return user_answer.strip().lower() == correct_answer.strip().lower()
    elif question_type == "essay":
        # Essay questions need manual grading
        return False
    return False

async def get_user_quiz_attempts(user_id: int, quiz_id: int, db: AsyncSession):
    """Get all attempts by a user for a specific quiz"""
    result = await db.execute(
        select(QuizAttempt).where(
            QuizAttempt.user_id == user_id,
            QuizAttempt.quiz_id == quiz_id
        ).order_by(QuizAttempt.completed_at.desc())
    )
    return result.scalars().all()

async def get_quiz_attempt_by_id(attempt_id: int, db: AsyncSession):
    """Get quiz attempt by ID"""
    result = await db.execute(
        select(QuizAttempt).where(QuizAttempt.id == attempt_id)
    )
    return result.scalar_one_or_none()
