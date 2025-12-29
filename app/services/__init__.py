"""
Services package - exports all services
"""
from services.user_service import create_user_service, get_user_by_id, update_user_service
from services.course_service import (
    create_course_service, get_course_by_id, update_course_service,
    delete_course_service, list_courses_service,
    create_lesson_service, get_lesson_by_id, update_lesson_service,
    get_course_lessons, enroll_user_in_course, get_user_enrollments,
    update_lesson_progress_service
)
from services.quiz_service import (
    create_quiz_service, get_quiz_by_id, update_quiz_service,
    delete_quiz_service, list_course_quizzes,
    create_question_service, get_question_by_id, update_question_service,
    get_quiz_questions, submit_quiz_attempt, get_user_quiz_attempts
)
from services.ai_service import ai_quiz_generator

__all__ = [
    # User services
    "create_user_service", "get_user_by_id", "update_user_service",
    # Course services
    "create_course_service", "get_course_by_id", "update_course_service",
    "delete_course_service", "list_courses_service",
    "create_lesson_service", "get_lesson_by_id", "update_lesson_service",
    "get_course_lessons", "enroll_user_in_course", "get_user_enrollments",
    "update_lesson_progress_service",
    # Quiz services
    "create_quiz_service", "get_quiz_by_id", "update_quiz_service",
    "delete_quiz_service", "list_course_quizzes",
    "create_question_service", "get_question_by_id", "update_question_service",
    "get_quiz_questions", "submit_quiz_attempt", "get_user_quiz_attempts",
    # AI services
    "ai_quiz_generator",
]
