# notesAPI

A simple REST API for managing notes, built with FastAPI and PostgreSQL.

## Stack

- Python
- FastAPI
- PostgreSQL
- SQLModel
- uvicorn

## Endpoints

| Method | Route | Description |
|---|---|---|
| GET | /notes | Get all notes |
| GET | /notes/{id} | Get a note by ID |
| POST | /notes | Create a note |
| PUT | /notes/{id} | Update a note |
| DELETE | /notes/{id} | Delete a note |

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies:
```bash
   uv sync
```
3. Create a `.env` file with your database URL:
