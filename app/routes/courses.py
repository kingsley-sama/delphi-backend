from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from models.course_model import (
    CourseCreate, CourseUpdate, CourseResponse,
    LessonCreate, LessonUpdate, LessonResponse,
    EnrollmentCreate, EnrollmentResponse,
    LessonProgressUpdate, LessonProgressResponse
)
from models.user_model import User
from services.course_service import (
    create_course_service, get_course_by_id, update_course_service,
    delete_course_service, list_courses_service,
    create_lesson_service, get_lesson_by_id, update_lesson_service,
    get_course_lessons, enroll_user_in_course, get_user_enrollments,
    update_lesson_progress_service
)
from utils.db import get_db
from utils.auth import get_current_active_user, require_role

course_router = APIRouter(prefix='/courses', tags=['Courses'])

# Course Endpoints
@course_router.post('/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Create a new course (admin/teacher only)"""
    course = await create_course_service(course_data, current_user.id, db)
    return CourseResponse(**course.model_dump())

@course_router.get('/', response_model=list[CourseResponse])
async def list_courses(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    subject: Optional[str] = None,
    grade_level: Optional[int] = None
):
    """List all published courses"""
    courses = await list_courses_service(db, skip, limit, subject, grade_level)
    return [CourseResponse(**course.model_dump()) for course in courses]

@course_router.get('/{course_id}', response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get course by ID"""
    course = await get_course_by_id(course_id, db)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return CourseResponse(**course.model_dump())

@course_router.put('/{course_id}', response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Update course (admin/teacher only)"""
    course = await update_course_service(course_id, course_update, db)
    return CourseResponse(**course.model_dump())

@course_router.delete('/{course_id}')
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Delete course (admin only)"""
    return await delete_course_service(course_id, db)

# Lesson Endpoints
@course_router.post('/{course_id}/lessons', response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Create a new lesson for a course (admin/teacher only)"""
    if lesson_data.course_id != course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course ID mismatch"
        )
    lesson = await create_lesson_service(lesson_data, db)
    return LessonResponse(**lesson.model_dump())

@course_router.get('/{course_id}/lessons', response_model=list[LessonResponse])
async def list_course_lessons(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all lessons for a course"""
    lessons = await get_course_lessons(course_id, db)
    return [LessonResponse(**lesson.model_dump()) for lesson in lessons]

@course_router.get('/lessons/{lesson_id}', response_model=LessonResponse)
async def get_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get lesson by ID"""
    lesson = await get_lesson_by_id(lesson_id, db)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    return LessonResponse(**lesson.model_dump())

@course_router.put('/lessons/{lesson_id}', response_model=LessonResponse)
async def update_lesson(
    lesson_id: int,
    lesson_update: LessonUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "teacher"]))
):
    """Update lesson (admin/teacher only)"""
    lesson = await update_lesson_service(lesson_id, lesson_update, db)
    return LessonResponse(**lesson.model_dump())

# Enrollment Endpoints
@course_router.post('/{course_id}/enroll', response_model=EnrollmentResponse)
async def enroll_in_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Enroll current user in a course"""
    enrollment = await enroll_user_in_course(current_user.id, course_id, db)
    return EnrollmentResponse(**enrollment.model_dump())

@course_router.get('/enrollments/me', response_model=list[EnrollmentResponse])
async def get_my_enrollments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's enrollments"""
    enrollments = await get_user_enrollments(current_user.id, db)
    return [EnrollmentResponse(**enrollment.model_dump()) for enrollment in enrollments]

# Progress Tracking Endpoints
@course_router.post('/lessons/{lesson_id}/progress', response_model=LessonProgressResponse)
async def update_lesson_progress(
    lesson_id: int,
    progress_update: LessonProgressUpdate,
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update lesson progress for current user"""
    progress = await update_lesson_progress_service(
        user_id=current_user.id,
        lesson_id=lesson_id,
        enrollment_id=enrollment_id,
        is_completed=progress_update.is_completed or False,
        time_spent=progress_update.time_spent_minutes or 0,
        db=db
    )
    return LessonProgressResponse(**progress.model_dump())
