# KPA Railway Management System (Backend API)

## Overview
manages railway wheel and bogie inspection data via REST API

## Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker & Docker Compose
- Postman

### Local (without Docker)
Install dependencies:
pip install fastapi uvicorn psycopg2-binary sqlalchemy pydantic

Ensure PostgreSQL is running and a database named kpa_erp is created with username/password.

Adjust DATABASE_URL in main.py if needed.

Start the API server:
uvicorn main:app --reload
Visit http://127.0.0.1:8000/docs for interactive API documentation.

### With Docker
1. Build and start everything (if you have docker-compose.yml ready):
docker-compose build
docker-compose up

2.The API will be available at http://localhost:8000.

See the exported Postman collection for example request and response payloads.

How to Test
Import the Postman collection into Postman.

Use the collection to test each endpoint (POST/GET).

Confirm that data is correctly stored in the kpa_erp PostgreSQL database.

Check http://localhost:8000/docs for built-in Swagger documentation and try requests there.

Troubleshooting & Notes
If database errors occur, double-check DATABASE_URL and PostgreSQL settings.

When using Docker, use db as the PostgreSQL host in your connection string.

For authentication or specific headers, refer to API documentation or Postman example.

If migrations or tables are missing, restart the API or use Alembic for migrations if needed.
