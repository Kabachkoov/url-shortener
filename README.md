""""URL Shortener REST API""""

A universal REST API for URL shortening service (similar to bit.ly) built with FastAPI, PostgreSQL, JWT authentication, and Celery for asynchronous tasks.

""Features""

    🔐 JWT Authentication - Secure user registration and login

    🔗 URL Shortening - Create custom or auto-generated short URLs

    📊 Analytics - Track click counts and last accessed timestamps

    📄 Pagination - Efficiently browse through lists of URLs

    🐳 Dockerized - Easy deployment with Docker and Docker Compose

    ⚡ Async Tasks - Daily cleanup of inactive URLs using Celery

    🧪 Testing - Comprehensive test suite with pytest

    📚 Auto-generated Docs - Interactive API documentation (Swagger/ReDoc)

    🔄 Database Migrations - Alembic for schema management

""Tech Stack""

    ⚡FastAPI - Modern Python web framework

    ⚡PostgreSQL - Relational database

    ⚡SQLAlchemy - ORM and database toolkit

    ⚡Celery & Redis - Asynchronous task queue and message broker

    ⚡JWT - JSON Web Tokens for authentication

    ⚡Pydantic - Data validation and settings management

    ⚡Docker & Docker Compose - Containerization and orchestration

    ⚡Pytest - Testing framework

    ⚡Alembic - Database migrations

""Quick Start""

-Prerequisites

    1)Docker and Docker Compose

    2)Python 3.11+ (for local development)

-Installation

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
