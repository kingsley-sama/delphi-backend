from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from models.user_model import User
from models.quiz_model import DifficultyLevel
from services.ai_service import ai_quiz_generator
from services.quiz_service import create_quiz_service, create_question_service
from models.quiz_model import QuizQuestionCreate
from utils.db import get_db
from utils.auth import get_current_active_user, require_role

ai_router = APIRouter(prefix='/ai', tags=['AI Services'])

class QuizGenerationRequest(BaseModel):
    topic: str
    subject: str
    grade_level: int
    num_questions: int = 10
    difficulty: DifficultyLevel = DifficultyLevel.medium
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None

class ContentEnhancementRequest(BaseModel):
    content: str
    grade_level: int

@ai_router.post('/generate-quiz')
async def generate_quiz_with_ai(
    request: QuizGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """
    Generate a quiz using AI (admin/teacher only)
    Creates the quiz and questions in the database
    """
    try:
        # Generate quiz using AI
        quiz_data = await ai_quiz_generator.generate_quiz(
            topic=request.topic,
            subject=request.subject,
            grade_level=request.grade_level,
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )
        
        # Create quiz in database
        from models.quiz_model import QuizCreate
        quiz_create = QuizCreate(
            course_id=request.course_id,
            lesson_id=request.lesson_id,
            title=quiz_data.get("title", f"Quiz: {request.topic}"),
            description=quiz_data.get("description", "AI-generated quiz"),
            difficulty_level=request.difficulty
        )
        
        quiz = await create_quiz_service(quiz_create, current_user.id, db)
        
        # Mark as AI generated
        quiz.is_ai_generated = True
        await db.commit()
        
        # Create questions
        questions_created = []
        for idx, q_data in enumerate(quiz_data.get("questions", [])):
            question_create = QuizQuestionCreate(
                quiz_id=quiz.id,
                question_text=q_data.get("question_text"),
                question_type=q_data.get("question_type", "multiple_choice"),
                options=q_data.get("options"),
                correct_answer=q_data.get("correct_answer"),
                explanation=q_data.get("explanation"),
                points=q_data.get("points", 1),
                order_index=idx
            )
            question = await create_question_service(question_create, db)
            questions_created.append(question)
        
        return {
            "message": "Quiz generated successfully",
            "quiz_id": quiz.id,
            "title": quiz.title,
            "num_questions": len(questions_created)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quiz: {str(e)}"
        )

@ai_router.post('/preview-quiz')
async def preview_generated_quiz(
    request: QuizGenerationRequest,
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """
    Preview AI-generated quiz without saving to database
    """
    try:
        quiz_data = await ai_quiz_generator.generate_quiz(
            topic=request.topic,
            subject=request.subject,
            grade_level=request.grade_level,
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )
        
        return {
            "preview": True,
            "quiz": quiz_data
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quiz preview: {str(e)}"
        )

@ai_router.post('/enhance-content')
async def enhance_content_with_ai(
    request: ContentEnhancementRequest,
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """
    Enhance educational content using AI (admin/teacher only)
    """
    try:
        enhanced_content = await ai_quiz_generator.enhance_content(
            content=request.content,
            grade_level=request.grade_level
        )
        
        return {
            "original_content": request.content,
            "enhanced_content": enhanced_content
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enhance content: {str(e)}"
        )

@ai_router.get('/status')
async def get_ai_service_status():
    """Check if AI services are available"""
    from core.config import settings
    
    is_configured = bool(settings.GEMINI_API_KEY)
    
    return {
        "ai_enabled": is_configured,
        "service": "Google Gemini" if is_configured else "Not configured",
        "features": [
            "Quiz Generation",
            "Content Enhancement",
            "Personalized Learning"
        ] if is_configured else []
    }
