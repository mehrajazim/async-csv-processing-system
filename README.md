# CSV to API Automation System

A FastAPI-based system for processing CSV files and converting them to API endpoints with Celery for background task processing.

## Features

- CSV file upload via REST API
- Background task processing with Celery
- SQLite database for job tracking
- RESTful API endpoints

## Prerequisites

- Python 3.8+
- Redis (for Celery)

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd csv-api-automation
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables** (optional)

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./app.db
```

## Running the Application

### Start Redis Server

Redis is required for Celery. Install and run Redis:

```bash
# On macOS with Homebrew
brew install redis
brew services start redis

# On Ubuntu/Debian
sudo apt-get install redis-server
redis-server
```

### Start Celery Worker

```bash
celery -A app.core.celery_app worker --loglevel=info
```

### Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/upload-csv/` | Upload a CSV file |

### Upload CSV

```bash
curl -X POST -F "file=@currency01.csv" http://localhost:8000/upload-csv/
```

## Project Structure

```
csv-api-automation/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Celery and config
│   ├── db/           # Database session and deps
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── main.py       # FastAPI app
├── uploads/          # Uploaded CSV files
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Technology Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Celery** - Task queue
- **Redis** - Message broker
- **Pandas** - CSV processing
- **Uvicorn** - ASGI server