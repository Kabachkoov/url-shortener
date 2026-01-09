""""URL Shortener REST API""""

A universal REST API for URL shortening service (similar to bit.ly) built with FastAPI, PostgreSQL, JWT authentication, and Celery for asynchronous tasks.

✨ Features
    🔐 JWT Authentication - Secure user registration and login
    🔗 URL Shortening - Create custom or auto-generated short URLs
    📊 Analytics - Track click counts and last accessed timestamps
    📄 Pagination - Efficiently browse through lists of URLs
    🐳 Dockerized - Easy deployment with Docker and Docker Compose
    ⚡ Async Tasks - Daily cleanup of inactive URLs using Celery
    🧪 Testing - Comprehensive test suite with pytest
    📚 Auto-generated Docs - Interactive API documentation (Swagger/ReDoc)
    🔄 Database Migrations - Alembic for schema management

🏗️ System Architecture
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   FastAPI       │◄───►│   PostgreSQL    │     │     Redis       │
│   Application   │     │   Database      │     │   Message Bus   │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
         │                                               │
         │ HTTP Requests                         Celery  │
         │                                       Workers │
         ▼                                               ▼
┌─────────────────┐                             ┌─────────────────┐
│                 │                             │                 │
│ Nginx (Optional)│                             │    Background   │
│  Reverse Proxy  │                             │      Tasks      │
│                 │                             │                 │
└─────────────────┘                             └─────────────────┘


🤖 Tech Stack
    ⚡FastAPI - Modern Python web framework
    ⚡PostgreSQL - Relational database
    ⚡SQLAlchemy - ORM and database toolkit
    ⚡Celery & Redis - Asynchronous task queue and message broker
    ⚡JWT - JSON Web Tokens for authentication
    ⚡Pydantic - Data validation and settings management
    ⚡Docker & Docker Compose - Containerization and orchestration
    ⚡Pytest - Testing framework
    ⚡Alembic - Database migrations

🚀 Quick Start
--Prerequisites--
    1)Docker and Docker Compose
    2)Python 3.11+ (for local development)
--Installation--
    1)Clone the repository
        git clone https://github.com/yourusername/url-shortener.git
        cd url-shortener
    2)Configure environment variables
        cp .env.example .env    # Edit .env file with your configuration if needed
    3)Build and start the application
        docker-compose up --build
    4)Run database migrations
        docker-compose exec web alembic upgrade head
    5)Access the application
    📄API Documentation: http://localhost:8000/docs
    📄Alternative Docs: http://localhost:8000/redoc
    📄API Base URL: http://localhost:8000/api/v1
    📄Health Check: http://localhost:8000/health

📖 API Usage Examples
    1)User Registration
       curl -X POST "http://localhost:8000/api/v1/auth/register" \
       -H "Content-Type: application/json" \
       -d '{"email": "user@example.com", "password": "securepassword"}'
    2)User Login
       curl -X POST "http://localhost:8000/api/v1/auth/login" \
       -H "Content-Type: application/json" \
       -d '{"email": "user@example.com", "password": "securepassword"}'
    3)Create Short URL
       curl -X POST "http://localhost:8000/api/v1/urls" \
       -H "Authorization: Bearer YOUR_JWT_TOKEN" \
       -H "Content-Type: application/json" \
      -d '{"original_url": "https://example.com/very/long/url/path", "custom_alias": "myalias"}'
    4)Access Short URL
       curl -X GET "http://localhost:8000/go/abc123" #Returns 308 Redirect to original URL
    5)Get URL Analytics
       curl -X GET "http://localhost:8000/api/v1/urls/abc123/stats" \
       -H "Authorization: Bearer YOUR_JWT_TOKEN"
 
🔧 Development Setup (Without Docker)
     1)Create virtual environment
       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate
     2)Install dependencies
       pip install -r requirements.txt
     3)Set up environment variables
       export DATABASE_URL="postgresql://user:password@localhost:5432/urlshortener"
       export SECRET_KEY="your-secret-key-here"
       export REDIS_URL="redis://localhost:6379/0"
     4)Initialize database
       alembic upgrade head
     5)Run the application
       uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
     6)Run background worker
       celery -A app.tasks.cleanup worker --loglevel=info

🧪 Running Tests
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_urls.py -v

🚀 Deployment
--Heroku--
  # Add Heroku PostgreSQL and Redis addons
  heroku addons:create heroku-postgresql:hobby-dev
  heroku addons:create heroku-redis:hobby-dev
  # Deploy application
  git push heroku main
  # Run migrations
  heroku run alembic upgrade head
--AWS Elastic Beanstalk--
  1)Configure Dockerrun.aws.json
  2)Set environment variables in AWS console
  3)Deploy using EB CLI
--Kubernetes--
  See kubernetes/ directory for sample deployments, services, and ingress configurations.

📈 Monitoring & Logging
    Application Logs: Structured JSON logging for production
    Health Checks: /health endpoint for service monitoring
    Performance Metrics: Integrated with Prometheus (optional)
    Error Tracking: Sentry integration (optional)

🔄 Background Tasks
The system includes a daily cleanup task that removes URLs not accessed in the last CLEANUP_DAYS (default: 90 days). This task:
    Runs daily at 2:00 AM UTC
    Identifies inactive URLs
    Performs soft deletion
    Logs cleanup statistics

🤝 Contributing
    Fork the repository
    Create a feature branch (git checkout -b feature/amazing-feature)
    Commit your changes (git commit -m 'Add amazing feature')
    Push to the branch (git push origin feature/amazing-feature)
    Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
    FastAPI community for the excellent framework
    SQLAlchemy and Alembic teams for database tools
    Docker community for containerization tools

📞 Support
For support, please open an issue in the GitHub repository or contact the maintainer.
