# Project Management App

A comprehensive FastAPI web application for managing projects and tasks with user authentication, dashboard analytics, and responsive UI.

## Features

- **User Authentication**: Secure login/registration with FastAPI-Users
- **Project Management**: Create, view, and manage projects
- **Task Management**: Create tasks, assign to projects, mark as complete
- **Dashboard**: View project statistics and task completion metrics
- **Responsive UI**: Built with Bootstrap 5.3 for all device sizes

## Technologies Used

- **Backend**: FastAPI, Python 3.8+
- **Database**: PostgreSQL (Azure compatible)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Authentication**: FastAPI-Users with cookie-based auth
- **Frontend**: Jinja2 Templates, Bootstrap 5.3
- **Deployment**: Compatible with Azure App Service

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- pip package manager

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/project-management-app.git
   cd project-management-app
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root:
   ```
   SECRET=your_secure_secret_key_here
   DATABASE_URL=postgresql+psycopg2://username:password@localhost/project_management_db
   ```

2. For Azure deployment, set these environment variables in the Azure App Service Configuration.

## Database Setup

1. Create PostgreSQL database:
   ```sql
   CREATE DATABASE project_management_db;
   ```

2. Initialize database tables:
   ```bash
   python -m app.tests.rebuild_postgres_db
   ```

3. Create a test user:
   ```bash
   python -m app.tests.create_test_user
   ```

## Running the Application

### Development Mode

```bash
fastapi dev app/main.py
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Azure Deployment

1. Create Azure PostgreSQL Flexible Server
2. Configure App Service with required environment variables
3. Deploy using Azure DevOps or GitHub Actions


## Usage

1. Navigate to `http://localhost:8000`
2. Login with test user or create a new account
3. Create projects and tasks
4. Track progress on the dashboard

## License

MIT