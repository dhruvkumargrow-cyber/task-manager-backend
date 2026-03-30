# Task Management REST API

A production-ready REST API for task management built with Flask and PostgreSQL.

## 🌐 Live API
**Base URL:** `https://task-manager-backend-production-ec4f.up.railway.app`

Try it: `curl https://task-manager-backend-production-ec4f.up.railway.app/health`

## Features
- Full CRUD operations (Create, Read, Update, Delete)
- PostgreSQL database integration
- Input validation and structured error responses
- 11 pytest unit tests — 100% passing
- CI/CD pipeline via GitHub Actions — green badge on repo
- Deployed on Railway (cloud)

## Tech Stack
Python · Flask · PostgreSQL · psycopg2 · pytest · GitHub Actions · Railway

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API info |
| GET | /health | Health check |
| GET | /tasks | Get all tasks |
| GET | /tasks/<id> | Get single task |
| POST | /tasks | Create a task |
| PUT | /tasks/<id> | Update a task |
| DELETE | /tasks/<id> | Delete a task |

## Task Status Values
- `pending`
- `in_progress`
- `completed`

## Setup
1. Clone the repo
2. Copy `config.example.py` to `config.py` and fill in your PostgreSQL credentials
3. Install dependencies: `pip install flask psycopg2-binary pytest gunicorn`
4. Create the table: `python setup_db.py`
5. Run the API: `python app.py`
6. Run tests: `python -m pytest test_app.py -v`