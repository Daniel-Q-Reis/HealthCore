@echo off

REM Switch to Docker settings
echo Switching to Docker settings...

REM Check if backup file exists
if exist "healthcore\settings\development.py.docker.bak" (
    REM Restore the Docker settings from backup
    copy "healthcore\settings\development.py.docker.bak" "healthcore\settings\development.py"
    del "healthcore\settings\development.py.docker.bak"
    echo Successfully switched to Docker settings.
) else (
    REM Update the development.py file to use 'db' instead of localhost for PostgreSQL
    powershell -Command "(gc healthcore\settings\development.py) -replace "'HOST': 'localhost'", "'HOST': 'db'" | Out-File -encoding ASCII healthcore\settings\development.py"
    echo Successfully switched to Docker settings.
)