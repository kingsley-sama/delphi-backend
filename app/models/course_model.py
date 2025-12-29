from sqlmodel import Field, SQLModel, Column, Relationship
from datetime import datetime
from pydantic import BaseModel
import sqlalchemy as sa
from enum import Enum
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.user_model import User
    from models.quiz_model import Quiz

class CourseTier(str, Enum):
    basic = "basic"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"

# Course Models
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    grade_level: int
    tier: CourseTier = CourseTier.basic
    thumbnail_url: Optional[str] = None

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    grade_level: Optional[int] = None
    tier: Optional[CourseTier] = None
    is_published: Optional[bool] = None
    thumbnail_url: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    subject: str
    grade_level: int
    tier: CourseTier
    created_by: Optional[int]
    is_published: bool
    thumbnail_url: Optional[str]
    created_at: datetime

class Course(SQLModel, table=True):
    __tablename__ = "courses"
    
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = Field(default=None)
    subject: str = Field(index=True)
    grade_level: int = Field(index=True)
    tier: CourseTier = Field(
        default=CourseTier.basic,
        sa_column=Column(sa.Enum(CourseTier, name="course_tier_enum"))
    )
    created_by: int | None = Field(default=None, foreign_key="user.id")
    is_published: bool = Field(default=False)
    thumbnail_url: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Lesson Models
class LessonCreate(BaseModel):
    course_id: int
    title: str
    content: Optional[str] = None
    order_index: int
    video_url: Optional[str] = None
    duration_minutes: Optional[int] = None

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    order_index: Optional[int] = None
    video_url: Optional[str] = None
    duration_minutes: Optional[int] = None

class LessonResponse(BaseModel):
    id: int
    course_id: int
    title: str
    content: Optional[str]
    order_index: int
    video_url: Optional[str]
    duration_minutes: Optional[int]
    created_at: datetime

class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"
    
    id: int | None = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    title: str
    content: str | None = Field(default=None)
    order_index: int
    video_url: str | None = Field(default=None)
    duration_minutes: int | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Course Enrollment Models
class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    completed_at: Optional[datetime]
    progress_percentage: float

class CourseEnrollment(SQLModel, table=True):
    __tablename__ = "course_enrollments"
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = Field(default=None)
    progress_percentage: float = Field(default=0.0)

# Lesson Progress Models
class LessonProgressCreate(BaseModel):
    lesson_id: int
    enrollment_id: int

class LessonProgressUpdate(BaseModel):
    is_completed: Optional[bool] = None
    time_spent_minutes: Optional[int] = None

class LessonProgressResponse(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    enrollment_id: int
    is_completed: bool
    time_spent_minutes: int
    completed_at: Optional[datetime]
    last_accessed_at: datetime

class LessonProgress(SQLModel, table=True):
    __tablename__ = "lesson_progress"
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    lesson_id: int = Field(foreign_key="lessons.id", index=True)
    enrollment_id: int = Field(foreign_key="course_enrollments.id")
    is_completed: bool = Field(default=False)
    time_spent_minutes: int = Field(default=0)
    completed_at: datetime | None = Field(default=None)
    last_accessed_at: datetime = Field(default_factory=datetime.utcnow)
