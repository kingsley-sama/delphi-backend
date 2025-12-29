"""
Models package - exports all models for easy importing
"""
from models.user_model import User, UserCreate, UserLogin, UserUpdate, UserResponse, UserRole
from models.course_model import (
    Course, CourseCreate, CourseUpdate, CourseResponse, CourseTier,
    Lesson, LessonCreate, LessonUpdate, LessonResponse,
    CourseEnrollment, EnrollmentCreate, EnrollmentResponse,
    LessonProgress, LessonProgressCreate, LessonProgressUpdate, LessonProgressResponse
)
from models.quiz_model import (
    Quiz, QuizCreate, QuizUpdate, QuizResponse,
    QuizQuestion, QuizQuestionCreate, QuizQuestionUpdate, QuizQuestionResponse,
    QuizAttempt, QuizAttemptCreate, QuizAttemptResponse,
    QuestionType, DifficultyLevel
)

__all__ = [
    # User models
    "User", "UserCreate", "UserLogin", "UserUpdate", "UserResponse", "UserRole",
    # Course models
    "Course", "CourseCreate", "CourseUpdate", "CourseResponse", "CourseTier",
    "Lesson", "LessonCreate", "LessonUpdate", "LessonResponse",
    "CourseEnrollment", "EnrollmentCreate", "EnrollmentResponse",
    "LessonProgress", "LessonProgressCreate", "LessonProgressUpdate", "LessonProgressResponse",
    # Quiz models
    "Quiz", "QuizCreate", "QuizUpdate", "QuizResponse",
    "QuizQuestion", "QuizQuestionCreate", "QuizQuestionUpdate", "QuizQuestionResponse",
    "QuizAttempt", "QuizAttemptCreate", "QuizAttemptResponse",
    "QuestionType", "DifficultyLevel",
]