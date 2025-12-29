# Delphi Educational Platform Backend

A comprehensive backend system for an AI-powered educational platform built with FastAPI, PostgreSQL, and Google Gemini AI.

## Features

### Core Functionality
- 🔐 **Authentication & Authorization** - JWT-based auth with role-based access control (Admin, Teacher, Parent, Learner)
- 👥 **User Management** - Complete user profile and account management
- 📚 **Course Management** - Create, organize, and publish courses with lessons
- 🎯 **Quiz System** - Comprehensive assessment system with multiple question types
- 📊 **Progress Tracking** - Track student progress and course completion
- 🤖 **AI-Powered Features** - Auto-generate quizzes and enhance content using Google Gemini

### User Roles
- **Admin** - Full system access and management
- **Teacher** - Create and manage courses, lessons, and quizzes
- **Parent** - Monitor learner progress (future enhancement)
- **Learner** - Enroll in courses, complete lessons, take quizzes

## Tech Stack

- **Framework**: FastAPI 0.123.9
- **Database**: PostgreSQL with AsyncPG
- **ORM**: SQLModel
- **Authentication**: JWT with bcrypt password hashing
- **AI Integration**: Google Gemini (gemini-pro)
- **Python**: 3.10+

## Project Structure

```
delphi-backend/
├── app/
│   ├── core/
│   │   └── config.py          # Application configuration
│   ├── models/
│   │   ├── user_model.py      # User models and schemas
│   │   ├── course_model.py    # Course, lesson, enrollment models
│   │   └── quiz_model.py      # Quiz and assessment models
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User management endpoints
│   │   ├── courses.py         # Course management endpoints
│   │   ├── quizzes.py         # Quiz and assessment endpoints
│   │   └── ai.py              # AI service endpoints
│   ├── services/
│   │   ├── user_service.py    # User business logic
│   │   ├── course_service.py  # Course business logic
│   │   ├── quiz_service.py    # Quiz business logic
│   │   └── ai_service.py      # AI integration service
│   ├── utils/
│   │   ├── db.py              # Database connection and session
│   │   ├── auth.py            # JWT and authentication utilities
│   │   └── hash_password.py   # Password hashing utilities
│   └── main.py                # Application entry point
├── migrations/
│   └── 001_initial_schema.sql # Database schema
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
├── run_migrations.sh          # Database migration script
└── README.md
```

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher
- pip and virtualenv

### 2. Clone and Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb delphi

# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
nano .env
```

Update the `.env` file with your configuration:
```env
DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/delphi
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
GEMINI_API_KEY=your-gemini-api-key  # Optional, for AI features
```

### 4. Run Migrations

```bash
# Make migration script executable
chmod +x run_migrations.sh

# Run migrations
./run_migrations.sh
```

Or manually:
```bash
psql postgresql://user:password@localhost:5432/delphi -f migrations/001_initial_schema.sql
```

### 5. Start the Server

```bash
# From the app directory
cd app
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --port 8000
```

The API will be available at: http://localhost:8000

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/login` - User login (returns JWT token)
- `POST /auth/refresh` - Refresh access token

### Users
- `POST /users/` - Register new user
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile
- `GET /users/{user_id}` - Get user by ID (admin/teacher)
- `GET /users/` - List all users (admin/teacher)

### Courses
- `POST /courses/` - Create course (admin/teacher)
- `GET /courses/` - List all published courses
- `GET /courses/{course_id}` - Get course details
- `PUT /courses/{course_id}` - Update course (admin/teacher)
- `DELETE /courses/{course_id}` - Delete course (admin)
- `POST /courses/{course_id}/enroll` - Enroll in course
- `GET /courses/enrollments/me` - Get user's enrollments

### Lessons
- `POST /courses/{course_id}/lessons` - Create lesson (admin/teacher)
- `GET /courses/{course_id}/lessons` - List course lessons
- `GET /courses/lessons/{lesson_id}` - Get lesson details
- `PUT /courses/lessons/{lesson_id}` - Update lesson (admin/teacher)
- `POST /courses/lessons/{lesson_id}/progress` - Update lesson progress

### Quizzes
- `POST /quizzes/` - Create quiz (admin/teacher)
- `GET /quizzes/{quiz_id}` - Get quiz details
- `PUT /quizzes/{quiz_id}` - Update quiz (admin/teacher)
- `DELETE /quizzes/{quiz_id}` - Delete quiz (admin/teacher)
- `GET /quizzes/course/{course_id}` - List course quizzes
- `POST /quizzes/{quiz_id}/questions` - Add question (admin/teacher)
- `GET /quizzes/{quiz_id}/questions` - List quiz questions
- `POST /quizzes/{quiz_id}/attempt` - Submit quiz attempt
- `GET /quizzes/{quiz_id}/attempts` - Get user's attempts

### AI Services
- `POST /ai/generate-quiz` - Generate quiz with AI (admin/teacher)
- `POST /ai/preview-quiz` - Preview AI-generated quiz (admin/teacher)
- `POST /ai/enhance-content` - Enhance content with AI (admin/teacher)
- `GET /ai/status` - Check AI service status

## Database Schema

### Main Tables
- **user** - User accounts and profiles
- **courses** - Course catalog
- **lessons** - Course lessons and content
- **course_enrollments** - User course enrollments
- **lesson_progress** - Lesson completion tracking
- **quizzes** - Quiz definitions
- **quiz_questions** - Quiz questions
- **quiz_attempts** - Quiz submission records

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
ruff check .
ruff format .
```

### Adding New Migrations

Create a new SQL file in the `migrations/` directory:
```bash
touch migrations/002_your_migration_name.sql
```

Run it manually:
```bash
psql $DATABASE_URL -f migrations/002_your_migration_name.sql
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | JWT secret key | Yes |
| `PORT` | Server port (default: 8000) | No |
| `DEBUG` | Debug mode (default: False) | No |
| `GEMINI_API_KEY` | Google Gemini API key | No (for AI features) |
| `CORS_ORIGINS` | Allowed CORS origins | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration (default: 30) | No |

## AI Features

The platform integrates with Google Gemini AI for:
- **Automated Quiz Generation** - Generate quizzes based on topic, subject, and difficulty
- **Content Enhancement** - Improve educational content for age-appropriateness
- **Personalized Learning** - Future: Adaptive quizzes based on student performance

To enable AI features, obtain a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey) and add it to your `.env` file.

## Security

- Passwords are hashed using bcrypt
- JWT tokens for stateless authentication
- Role-based access control (RBAC)
- SQL injection protection via SQLModel/SQLAlchemy
- CORS middleware for cross-origin security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on the repository.

---

Built with ❤️ for education
