# Road Safety Management Platform

An analytical platform for city-level road safety management, enabling evidence-based decisions through strategic intervention tracking and analysis.

## Product Vision

To become the standard analytical platform for city-level road safety management, enabling evidence-based decisions that value every life equally and demonstrate measurable impact through strategic intervention.

## Target Audience

- Transport department officials
- Traffic police officers
- Urban planners responsible for road safety decisions and infrastructure investments in cities with high accident rates

## Core Features

- **CRUD Operations for Road Incidents**: Create, read, update, and delete road incident records
- **Incident Tracking**: Track accidents with detailed information including location, severity, casualties, and conditions
- **Data Analysis**: Filter and query incidents by type, severity, and other parameters

## Technology Stack

- **Backend Framework**: FastAPI 0.104.1
- **Database**: SQLite (SQLAlchemy ORM)
- **Data Validation**: Pydantic 2.5.0
- **Server**: Uvicorn
- **Architecture**: Modular Monolith

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository or navigate to the project directory

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

5. Create environment file:
```bash
cp .env.example .env
```

6. Edit `.env` file and update configuration as needed (especially `SECRET_KEY` for production)

## Running the Application

### Development Mode

Run the application with auto-reload enabled:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Production Mode

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Incidents Management
- `POST /api/v1/incidents` - Create a new incident
- `GET /api/v1/incidents` - Get all incidents (with optional filtering)
- `GET /api/v1/incidents/{incident_id}` - Get a specific incident
- `PUT /api/v1/incidents/{incident_id}` - Update an incident
- `DELETE /api/v1/incidents/{incident_id}` - Delete an incident

### Query Parameters for GET /api/v1/incidents
- `skip` - Number of records to skip (default: 0)
- `limit` - Maximum number of records to return (default: 100)
- `severity` - Filter by severity level
- `incident_type` - Filter by incident type

## Example API Usage

### Create an Incident

```bash
curl -X POST "http://localhost:8000/api/v1/incidents" \
  -H "Content-Type: application/json" \
  -d '{
    "incident_type": "collision",
    "severity": "major",
    "location": "Main Street and 5th Avenue",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "description": "Two-vehicle collision at intersection",
    "date_time": "2026-09-12T10:30:00",
    "casualties": 2,
    "vehicles_involved": 2,
    "weather_conditions": "clear",
    "road_conditions": "dry"
  }'
```

### Get All Incidents

```bash
curl -X GET "http://localhost:8000/api/v1/incidents"
```

### Get Incidents by Severity

```bash
curl -X GET "http://localhost:8000/api/v1/incidents?severity=major"
```

### Update an Incident

```bash
curl -X PUT "http://localhost:8000/api/v1/incidents/1" \
  -H "Content-Type: application/json" \
  -d '{
    "casualties": 3,
    "description": "Updated: Three casualties confirmed"
  }'
```

### Delete an Incident

```bash
curl -X DELETE "http://localhost:8000/api/v1/incidents/1"
```

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup and session management
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── __init__.py
│       └── incidents.py     # Incident CRUD endpoints
├── .env.example             # Example environment variables
└── README.md               # This file
```

## Database Schema

### RoadIncident Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| incident_type | String | Type of incident (e.g., collision, pedestrian accident) |
| severity | String | Severity level (minor, major, fatal) |
| location | String | Location description |
| latitude | Float | Latitude coordinate (optional) |
| longitude | Float | Longitude coordinate (optional) |
| description | Text | Detailed description (optional) |
| date_time | DateTime | Date and time of incident |
| casualties | Integer | Number of casualties |
| vehicles_involved | Integer | Number of vehicles involved |
| weather_conditions | String | Weather conditions (optional) |
| road_conditions | String | Road conditions (optional) |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

## Environment Variables

See `.env.example` for all available configuration options:

- `APP_NAME` - Application name
- `DEBUG` - Debug mode (True/False)
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for security (change in production!)
- `ALLOWED_ORIGINS` - CORS allowed origins
- `API_V1_PREFIX` - API version prefix

## Security Considerations

- Change `SECRET_KEY` in production environment
- Use PostgreSQL or MySQL for production instead of SQLite
- Implement authentication and authorization for production use
- Enable HTTPS in production
- Configure appropriate CORS origins
- Implement rate limiting for API endpoints

## Development

### Adding New Features

1. Create new models in `backend/models.py`
2. Create corresponding schemas in `backend/schemas.py`
3. Create router files in `backend/routers/`
4. Register routers in `backend/main.py`

### Database Migrations

For production use, consider implementing Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
```

## License

This project is part of a road safety management initiative.
