@echo off

REM Setup script for the Pharmacy API project on Windows

echo Setting up the Pharmacy API development environment...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install pre-commit hooks
echo Installing pre-commit hooks...
pre-commit install

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
)

echo Local setup complete. Pre-commit hooks are installed.
echo To run the project, use the Docker scripts (e.g., scripts\run_docker.bat).