# Delphi Backend - Quick Reference

## Quick Start Commands

```bash
# Setup (first time)
./setup.sh

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
./run_migrations.sh

# Start development server
cd app && python main.py

# Or with uvicorn
uvicorn app.main:app --reload --port 8000
```

## Database Commands

```bash
# Create database
createdb delphi

# Run migration
psql postgresql://user:pass@localhost:5432/delphi -f migrations/001_initial_schema.sql

# Connect to database
psql postgresql://user:pass@localhost:5432/delphi

# Drop and recreate (CAUTION!)
dropdb delphi && createdb delphi
```

## API Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app

# Run specific test
pytest tests/test_api.py::TestAuth::test_login_success
```

## Common API Calls (with curl)

### Register User
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "student1",
    "email": "student@example.com",
    "password": "SecurePass123!",
    "age": 16,
    "grade_level": 10
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student@example.com&password=SecurePass123!"
```

### Create Course (with token)
```bash
curl -X POST http://localhost:8000/courses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Introduction to Python",
    "description": "Learn Python basics",
    "subject": "Computer Science",
    "grade_level": 10,
    "tier": "basic"
  }'
```

### Generate AI Quiz
```bash
curl -X POST http://localhost:8000/ai/generate-quiz \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "topic": "Python Variables",
    "subject": "Computer Science",
    "grade_level": 10,
    "num_questions": 5,
    "difficulty": "medium"
  }'
```

## Project Structure Overview

```
app/
├── main.py              # App entry point, router setup
├── core/
│   └── config.py        # Settings and configuration
├── models/              # Database models (SQLModel)
│   ├── user_model.py
│   ├── course_model.py
│   └── quiz_model.py
├── routes/              # API endpoints (FastAPI routers)
│   ├── auth.py
│   ├── users.py
│   ├── courses.py
│   ├── quizzes.py
│   └── ai.py
├── services/            # Business logic
│   ├── user_service.py
│   ├── course_service.py
│   ├── quiz_service.py
│   └── ai_service.py
└── utils/               # Utilities
    ├── db.py           # Database connection
    ├── auth.py         # JWT utilities
    └── hash_password.py # Password hashing
```

## Key Features Implemented

✅ User authentication (JWT)
✅ Role-based access control (Admin, Teacher, Parent, Learner)
✅ Course management (CRUD)
✅ Lesson management with progress tracking
✅ Quiz system with multiple question types
✅ Automated quiz grading
✅ AI-powered quiz generation (Google Gemini)
✅ Content enhancement with AI
✅ Course enrollment system
✅ Progress tracking per lesson
✅ RESTful API design
✅ Comprehensive database schema

## Environment Variables Required

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/delphi
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-key  # Optional
PORT=8000
DEBUG=True
```

## Next Steps / Future Enhancements

- [ ] Add parent dashboard functionality
- [ ] Implement personalized learning paths
- [ ] Add video upload/streaming support
- [ ] Create analytics dashboard
- [ ] Add email notifications
- [ ] Implement real-time chat/discussion
- [ ] Add file attachment support for lessons
- [ ] Create mobile API endpoints
- [ ] Add social learning features
- [ ] Implement gamification (badges, points)

## Troubleshooting

### Database connection errors
- Check DATABASE_URL format
- Ensure PostgreSQL is running
- Verify database exists

### JWT errors
- Ensure SECRET_KEY is set in .env
- Check token expiration (default 30 min)
- Verify Authorization header format: "Bearer <token>"

### AI features not working
- Check GEMINI_API_KEY is set
- Verify API key is valid
- Check API quota limits

## Support

API Documentation: http://localhost:8000/docs
Health Check: http://localhost:8000/health
AI Status: http://localhost:8000/ai/status
