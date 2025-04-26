# Employee Data Generation & Visualization (Docker + Flask + SQLite)

This Flask application generates synthetic employee data, stores it in an SQLite database, and provides REST API endpoints for analytical summaries along with visualizations.

## Features

- **Data Generation**: Creates synthetic employee data with departments, job titles, salaries, and performance ratings.
- **SQLite Integration**: Lightweight relational database for easy setup and portability.
- **REST API Endpoints**: Provides endpoints to retrieve analytical summaries and insights.
- **Data Visualization**: Interactive charts built with Chart.js.
- **Swagger UI**: Easy-to-use API documentation and testing interface.
- **Docker Support**: Fully containerized for consistent development and deployment.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed
- (Optional) Python 3.7+ if running locally without Docker

### Installation (Docker)

1. Clone the repository (or download and extract the ZIP file)

2. Build the Docker image:

   ```bash
   docker build -t employee-data-app .
   ```

3. Run the container:

   ```bash
   docker run -p 5000:5000 employee-data-app
   ```

4. Open your browser and navigate to `http://localhost:5000`

5. Use the web interface to generate data and view visualizations.

---

### Installation (Local Setup without Docker)

1. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables (optional):

   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   ```

4. Run the application:

   ```bash
   flask run
   ```

5. Access it at `http://localhost:5000`

---

## API Documentation

Swagger UI is available at:

```
http://localhost:5000/swagger
```

You can explore and test all API endpoints directly from the browser.

---

## Core Components

- **Data Generation**: Randomized, realistic employee data generation.
- **Database**: Lightweight and serverless SQLite database (`employee.db` file).
- **API Endpoints**: RESTful services to fetch, analyze, and visualize data.
- **Data Visualization**: Interactive charts for salary, departments, performance ratings, and tenure.

---

## API Endpoints Overview

### Data Generation
- `POST /api/generate-data` — Generate synthetic employee data.

### Data Retrieval
- `GET /api/employees` — Get all employees (paginated).
- `GET /api/employees/{id}` — Get employee details by ID.
- `GET /api/departments` — List all departments.
- `GET /api/departments/{id}/employees` — List employees within a department.

### Analytics
- `GET /api/analytics/employees-by-department` — Employee count by department.
- `GET /api/analytics/salary-distribution` — Salary distribution statistics.
- `GET /api/analytics/tenure-distribution` — Employee tenure distribution.
- `GET /api/analytics/performance-by-department` — Performance by department.

### Visualizations
- `GET /api/visualizations/employees-by-department` — Department-wise employee chart.
- `GET /api/visualizations/salary-distribution` — Salary distribution chart.

---

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models (Employee, Department)
│   ├── routes.py            # REST API routes
│   ├── data_generator.py    # Data generation logic
│   ├── static/              # Static assets (e.g., Swagger JSON, JS, CSS)
│   │   └── swagger.json     # Swagger API documentation
│   └── templates/           # HTML templates
│       └── index.html       # Dashboard UI
├── config.py                # App configuration settings
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker build configuration
└── .flaskenv                # Flask environment settings
```

---

## Future Improvements

- User authentication and authorization for restricted endpoints
- Advanced filtering, search, and sorting capabilities
- Exporting reports as PDF or Excel
- Live dashboards with real-time updates
- Scalable database backend option (e.g., PostgreSQL, MySQL)
- Full Docker Compose setup for multi-container deployments

---

## Notes

- By default, the application uses an SQLite database stored as `employee.db` inside the Docker container.
- Database migrations are handled automatically using **Flask-Migrate**.
- Ideal for demos, prototypes, and small-scale analytics projects!