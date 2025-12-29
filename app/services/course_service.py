from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.course_model import (
    Course, CourseCreate, CourseUpdate,
    Lesson, LessonCreate, LessonUpdate,
    CourseEnrollment, LessonProgress
)
from models.user_model import User

async def create_course_service(course_data: CourseCreate, creator_id: int, db: AsyncSession):
    """Create a new course"""
    new_course = Course(
        title=course_data.title,
        description=course_data.description,
        subject=course_data.subject,
        grade_level=course_data.grade_level,
        tier=course_data.tier,
        created_by=creator_id,
        thumbnail_url=course_data.thumbnail_url
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

async def get_course_by_id(course_id: int, db: AsyncSession):
    """Get course by ID"""
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )
    return result.scalar_one_or_none()

async def update_course_service(course_id: int, course_update: CourseUpdate, db: AsyncSession):
    """Update course information"""
    course = await get_course_by_id(course_id, db)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    update_data = course_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    
    await db.commit()
    await db.refresh(course)
    return course

async def delete_course_service(course_id: int, db: AsyncSession):
    """Delete a course"""
    course = await get_course_by_id(course_id, db)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    await db.delete(course)
    await db.commit()
    return {"message": "Course deleted successfully"}

async def list_courses_service(db: AsyncSession, skip: int = 0, limit: int = 100, 
                               subject: str = None, grade_level: int = None):
    """List courses with optional filters"""
    query = select(Course).where(Course.is_published == True)
    
    if subject:
        query = query.where(Course.subject == subject)
    if grade_level:
        query = query.where(Course.grade_level == grade_level)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Lesson Services
async def create_lesson_service(lesson_data: LessonCreate, db: AsyncSession):
    """Create a new lesson"""
    # Verify course exists
    course = await get_course_by_id(lesson_data.course_id, db)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    new_lesson = Lesson(
        course_id=lesson_data.course_id,
        title=lesson_data.title,
        content=lesson_data.content,
        order_index=lesson_data.order_index,
        video_url=lesson_data.video_url,
        duration_minutes=lesson_data.duration_minutes
    )
    db.add(new_lesson)
    await db.commit()
    await db.refresh(new_lesson)
    return new_lesson

async def get_lesson_by_id(lesson_id: int, db: AsyncSession):
    """Get lesson by ID"""
    result = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    return result.scalar_one_or_none()

async def update_lesson_service(lesson_id: int, lesson_update: LessonUpdate, db: AsyncSession):
    """Update lesson information"""
    lesson = await get_lesson_by_id(lesson_id, db)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    update_data = lesson_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lesson, key, value)
    
    await db.commit()
    await db.refresh(lesson)
    return lesson

async def get_course_lessons(course_id: int, db: AsyncSession):
    """Get all lessons for a course"""
    result = await db.execute(
        select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order_index)
    )
    return result.scalars().all()

# Enrollment Services
async def enroll_user_in_course(user_id: int, course_id: int, db: AsyncSession):
    """Enroll a user in a course"""
    # Check if course exists
    course = await get_course_by_id(course_id, db)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if already enrolled
    result = await db.execute(
        select(CourseEnrollment).where(
            CourseEnrollment.user_id == user_id,
            CourseEnrollment.course_id == course_id
        )
    )
    existing_enrollment = result.scalar_one_or_none()
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )
    
    new_enrollment = CourseEnrollment(
        user_id=user_id,
        course_id=course_id
    )
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)
    return new_enrollment

async def get_user_enrollments(user_id: int, db: AsyncSession):
    """Get all enrollments for a user"""
    result = await db.execute(
        select(CourseEnrollment).where(CourseEnrollment.user_id == user_id)
    )
    return result.scalars().all()

async def update_lesson_progress_service(
    user_id: int, 
    lesson_id: int, 
    enrollment_id: int,
    is_completed: bool,
    time_spent: int,
    db: AsyncSession
):
    """Update or create lesson progress"""
    # Check if progress exists
    result = await db.execute(
        select(LessonProgress).where(
            LessonProgress.user_id == user_id,
            LessonProgress.lesson_id == lesson_id
        )
    )
    progress = result.scalar_one_or_none()
    
    if progress:
        # Update existing progress
        progress.is_completed = is_completed
        progress.time_spent_minutes += time_spent
        if is_completed and not progress.completed_at:
            from datetime import datetime
            progress.completed_at = datetime.utcnow()
    else:
        # Create new progress
        from datetime import datetime
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            enrollment_id=enrollment_id,
            is_completed=is_completed,
            time_spent_minutes=time_spent,
            completed_at=datetime.utcnow() if is_completed else None
        )
        db.add(progress)
    
    await db.commit()
    await db.refresh(progress)
    
    # Update enrollment progress
    await update_enrollment_progress(enrollment_id, db)
    
    return progress

async def update_enrollment_progress(enrollment_id: int, db: AsyncSession):
    """Calculate and update enrollment progress percentage"""
    result = await db.execute(
        select(CourseEnrollment).where(CourseEnrollment.id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    
    if not enrollment:
        return
    
    # Get total lessons
    lessons_result = await db.execute(
        select(Lesson).where(Lesson.course_id == enrollment.course_id)
    )
    total_lessons = len(lessons_result.scalars().all())
    
    if total_lessons == 0:
        return
    
    # Get completed lessons
    progress_result = await db.execute(
        select(LessonProgress).where(
            LessonProgress.enrollment_id == enrollment_id,
            LessonProgress.is_completed == True
        )
    )
    completed_lessons = len(progress_result.scalars().all())
    
    # Update progress percentage
    enrollment.progress_percentage = (completed_lessons / total_lessons) * 100
    
    # Mark as completed if all lessons done
    if completed_lessons == total_lessons:
        from datetime import datetime
        enrollment.completed_at = datetime.utcnow()
    
    await db.commit()
