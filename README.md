# Card Access Logging System

A Python application to log entry and exit times based on card IDs.
This version uses **PostgreSQL** and provides both a **FastAPI Service** and a **CLI Tool**.

## Features
- **PostgreSQL Database**: Persistent storage for users and logs.
- **FastAPI Service**: REST API for managing users and scans.
- **CLI Tool**: Command-line interface for local testing.
- **Automatic Status Toggle**: Automatically detects 'ENTRY' or 'EXIT'.

## Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The database connection is configured in `database.py`.
Current default: `postgresql://postgres:6eEZzlFtdjI85h1uaBMBu5BXXkgUMWr8umEvpz0FAhYjOlnrnkZuz33tW6Eoftok@93.177.102.172:5432/postgres`

## Running the API Service

Start the server using `uvicorn`:

```bash
uvicorn main:app --reload
```

- **Docs**: Open http://127.0.0.1:8000/docs for the interactive API documentation.
- **Root**: http://127.0.0.1:8000/

### API Endpoints
- `POST /scan`: Scan a card `{ "card_id": "..." }`.
- `POST /users`: Register a user `{ "card_id": "...", "full_name": "..." }`.
- `GET /history`: View access logs.
- `GET /users/{card_id}`: Get user details.

## Running the CLI Tool

For local testing/simulation via terminal:

```bash
python cli.py
```

## Default User
The system handles registration. You can create a test user via API or CLI:
- **ID**: `00x-abc-bcd`
- **Name**: `Furkan Ulutaş`
