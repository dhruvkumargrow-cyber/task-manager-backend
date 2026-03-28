# Task Management REST API

A fully functional REST API for task management built with Flask and PostgreSQL.

## Features
- Full CRUD operations (Create, Read, Update, Delete)
- PostgreSQL database integration
- Input validation and structured error responses
- 11 unit tests with pytest — 100% passing
- REST best practices (correct HTTP methods and status codes)

## Tech Stack
Python · Flask · PostgreSQL · psycopg2 · pytest

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /tasks | Get all tasks |
| GET | /tasks/<id> | Get single task |
| POST | /tasks | Create a task |
| PUT | /tasks/<id> | Update a task |
| DELETE | /tasks/<id> | Delete a task |

## Setup
1. Clone the repo
2. Copy `config.example.py` to `config.py` and fill in your PostgreSQL credentials
3. Install dependencies: `pip install flask psycopg2-binary pytest`
4. Create the table: `python setup_db.py`
5. Run the API: `python app.py`
6. Run tests: `python -m pytest test_app.py -v`

## Task Status Values
- `pending`
- `in_progress`
- `completed`