from sqlmodel import Field, SQLModel, Column, Relationship
from datetime import datetime
from pydantic import BaseModel
import sqlalchemy as sa
from enum import Enum
from typing import Optional, List, Dict, Any
from sqlalchemy.dialects.postgresql import JSONB

class QuestionType(str, Enum):
    multiple_choice = "multiple_choice"
    true_false = "true_false"
    short_answer = "short_answer"
    essay = "essay"

class DifficultyLevel(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

# Quiz Models
class QuizCreate(BaseModel):
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    passing_score: int = 70
    difficulty_level: DifficultyLevel = DifficultyLevel.medium

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    passing_score: Optional[int] = None
    difficulty_level: Optional[DifficultyLevel] = None

class QuizResponse(BaseModel):
    id: int
    course_id: Optional[int]
    lesson_id: Optional[int]
    title: str
    description: Optional[str]
    time_limit_minutes: Optional[int]
    passing_score: int
    difficulty_level: DifficultyLevel
    is_ai_generated: bool
    created_by: Optional[int]
    created_at: datetime

class Quiz(SQLModel, table=True):
    __tablename__ = "quizzes"
    
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default=None, foreign_key="courses.id", index=True)
    lesson_id: int | None = Field(default=None, foreign_key="lessons.id")
    title: str
    description: str | None = Field(default=None)
    time_limit_minutes: int | None = Field(default=None)
    passing_score: int = Field(default=70)
    difficulty_level: DifficultyLevel = Field(
        default=DifficultyLevel.medium,
        sa_column=Column(sa.Enum(DifficultyLevel, name="difficulty_level_enum"))
    )
    is_ai_generated: bool = Field(default=False)
    created_by: int | None = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Quiz Question Models
class QuizQuestionCreate(BaseModel):
    quiz_id: int
    question_text: str
    question_type: QuestionType = QuestionType.multiple_choice
    options: Optional[Dict[str, Any]] = None
    correct_answer: str
    explanation: Optional[str] = None
    points: int = 1
    order_index: int

class QuizQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[QuestionType] = None
    options: Optional[Dict[str, Any]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    points: Optional[int] = None
    order_index: Optional[int] = None

class QuizQuestionResponse(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    question_type: QuestionType
    options: Optional[Dict[str, Any]]
    correct_answer: str
    explanation: Optional[str]
    points: int
    order_index: int

class QuizQuestion(SQLModel, table=True):
    __tablename__ = "quiz_questions"
    
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quizzes.id", index=True)
    question_text: str
    question_type: QuestionType = Field(
        default=QuestionType.multiple_choice,
        sa_column=Column(sa.Enum(QuestionType, name="question_type_enum"))
    )
    options: Dict[str, Any] | None = Field(default=None, sa_column=Column(JSONB))
    correct_answer: str
    explanation: str | None = Field(default=None)
    points: int = Field(default=1)
    order_index: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Quiz Attempt Models
class QuizAttemptCreate(BaseModel):
    quiz_id: int
    answers: Dict[str, Any]

class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    score: int
    total_points: int
    percentage: float
    answers: Dict[str, Any]
    time_taken_minutes: Optional[int]
    passed: bool
    started_at: datetime
    completed_at: datetime

class QuizAttempt(SQLModel, table=True):
    __tablename__ = "quiz_attempts"
    
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quizzes.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    score: int
    total_points: int
    percentage: float
    answers: Dict[str, Any] = Field(sa_column=Column(JSONB))
    time_taken_minutes: int | None = Field(default=None)
    passed: bool
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime = Field(default_factory=datetime.utcnow)
