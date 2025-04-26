@echo off
echo Employee Data Generation & Visualization

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create static folder if it doesn't exist
if not exist app\static (
    echo Creating static folder...
    mkdir app\static
)

REM Copy swagger.json to static folder
echo Setting up Swagger UI...
if exist app\static\swagger.json (
    copy app\static\swagger.json app\static\swagger.json >nul
)

REM Create templates folder if it doesn't exist
if not exist app\templates (
    echo Creating templates folder...
    mkdir app\templates
)

REM Run the application
echo Starting the application...
set FLASK_APP=run.py
set FLASK_ENV=development
python run.py

pause
