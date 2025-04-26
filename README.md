# Employee Data Generation & Visualization

This Flask application generates synthetic employee data, stores it in a PostgreSQL database, and provides REST API endpoints to retrieve analytical summaries along with visualizations.

## Features

- **Data Generation**: Creates synthetic employee data with departments, job titles, salaries, and performance ratings.
- **PostgreSQL Integration**: Stores data in a relational database.
- **REST API Endpoints**: Provides endpoints to retrieve analytical summaries.
- **Data Visualization**: Uses Chart.js to visualize data with interactive charts.
- **Swagger UI**: API documentation and testing interface.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- PostgreSQL database

### Installation

1. Clone this repository (or download and extract the zip file)

2. Create a virtual environment and activate it
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database
   - Create a database named `employee_db`
   - Update database connection string in `config.py` if needed

5. Set environment variables (optional)
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   ```

### Running the Application

1. Run the Flask application
   ```bash
   python run.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Generate data using the web interface

### API Documentation

API documentation is available at `http://localhost:5000/swagger`

## Core Components

- **Data Generation**: Random but realistic employee data with appropriate distributions of salaries, departments, etc.
- **Database Design**: Relational model with departments and employees tables.
- **API Endpoints**: RESTful API for retrieving data and analytics.
- **Data Visualization**: Interactive charts for visualizing employee data.

## API Endpoints

### Data Generation
- `POST /api/generate-data` - Generate synthetic employee data

### Data Retrieval
- `GET /api/employees` - Get all employees (paginated)
- `GET /api/employees/{id}` - Get employee by ID
- `GET /api/departments` - Get all departments
- `GET /api/departments/{id}/employees` - Get employees by department

### Analytics
- `GET /api/analytics/employees-by-department` - Employee count by department
- `GET /api/analytics/salary-distribution` - Salary distribution statistics
- `GET /api/analytics/tenure-distribution` - Employee tenure distribution
- `GET /api/analytics/performance-by-department` - Performance ratings by department

### Visualizations
- `GET /api/visualizations/employees-by-department` - Department distribution chart
- `GET /api/visualizations/salary-distribution` - Salary distribution chart

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── routes.py            # API endpoints
│   ├── data_generator.py    # Synthetic data generator
│   ├── static/              # Static files
│   │   └── swagger.json     # Swagger API documentation
│   └── templates/           # HTML templates
│       └── index.html       # Dashboard UI
├── config.py               # Configuration settings
├── run.py                  # Application entry point
└── requirements.txt        # Dependencies
```

## Future Improvements

- Authentication and authorization
- More advanced filtering and search capabilities
- Additional data visualizations
- Performance optimizations for large datasets